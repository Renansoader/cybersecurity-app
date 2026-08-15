"""Camada SQLite: tentativas, SRS, status de módulo, sessões e desafios.

Regra central do app: só a primeira tentativa de cada questão conta no domínio.
Isso não fica a cargo do código de tela. O índice único parcial
`idx_primeira_tentativa` faz o próprio banco recusar uma segunda linha com
n_tentativa = 1 para a mesma questão — o erro estoura em vez de a estatística
inflar em silêncio.

Nenhuma view fala com o sqlite3 direto; tudo passa por aqui.
"""

import sqlite3
from contextlib import contextmanager
from datetime import date
from pathlib import Path

CAMINHO = Path(__file__).resolve().parent.parent / "progress.db"

ESQUEMA = """
-- Uma linha por tentativa. A primeira tentativa é imutável.
CREATE TABLE IF NOT EXISTS tentativas (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  questao_id    TEXT    NOT NULL,
  modulo_id     TEXT    NOT NULL,
  tipo          TEXT    NOT NULL,
  acertou       INTEGER NOT NULL,      -- 0 ou 1
  usou_dica     INTEGER NOT NULL,      -- 0 ou 1
  n_tentativa   INTEGER NOT NULL,      -- 1 = a que conta no domínio
  segundos      INTEGER NOT NULL,
  data          TEXT    NOT NULL       -- ISO 8601
);

-- O banco garante que existe no máximo uma "primeira tentativa" por questão.
CREATE UNIQUE INDEX IF NOT EXISTS idx_primeira_tentativa
ON tentativas(questao_id) WHERE n_tentativa = 1;

-- Estado do SRS por questão. Chave única de verdade.
CREATE TABLE IF NOT EXISTS srs (
  questao_id    TEXT PRIMARY KEY,
  modulo_id     TEXT NOT NULL,
  intervalo     REAL NOT NULL DEFAULT 1,
  facilidade    REAL NOT NULL DEFAULT 2.5,
  proxima_data  TEXT NOT NULL,
  acertos       INTEGER NOT NULL DEFAULT 0,
  erros         INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS modulos_status (
  modulo_id     TEXT PRIMARY KEY,
  desbloqueado  INTEGER NOT NULL DEFAULT 0,
  concluido     INTEGER NOT NULL DEFAULT 0,
  dominio       REAL    NOT NULL DEFAULT 0,   -- 0 a 1, só 1as tentativas
  atualizado_em TEXT
);

CREATE TABLE IF NOT EXISTS sessoes (
  data          TEXT PRIMARY KEY,      -- YYYY-MM-DD
  questoes      INTEGER NOT NULL DEFAULT 0,
  acertos       INTEGER NOT NULL DEFAULT 0,
  minutos       INTEGER NOT NULL DEFAULT 0,
  meta_batida   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS desafios_status (
  desafio_id    TEXT PRIMARY KEY,
  itens_ok      TEXT,                  -- JSON com os itens do checklist marcados
  concluido     INTEGER NOT NULL DEFAULT 0,
  data          TEXT
);
"""


@contextmanager
def conexao():
    """Abre, entrega, commita e fecha. Se der exceção, não commita."""
    con = sqlite3.connect(CAMINHO)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def iniciar():
    """Cria o banco e o esquema se ainda não existirem."""
    with conexao() as con:
        con.executescript(ESQUEMA)


def _hoje():
    return date.today().isoformat()


def registrar_tentativa(questao_id, modulo_id, tipo, acertou, usou_dica, segundos):
    """Grava uma tentativa e devolve qual número de tentativa ela foi.

    O `n_tentativa` é contado aqui, a partir do que já existe no banco — quem
    chama não passa esse número, justamente para não conseguir forjar uma
    "primeira tentativa". Se ainda assim uma segunda primeira chegar ao banco,
    o índice único parcial levanta sqlite3.IntegrityError.
    """
    with conexao() as con:
        # MAX + 1, e não COUNT + 1: se uma linha do meio for apagada, COUNT
        # devolveria um número já usado e duas tentativas ficariam com o mesmo
        # n_tentativa.
        ultima = con.execute(
            "SELECT COALESCE(MAX(n_tentativa), 0) FROM tentativas WHERE questao_id = ?",
            (questao_id,),
        ).fetchone()[0]
        n_tentativa = ultima + 1
        con.execute(
            "INSERT INTO tentativas (questao_id, modulo_id, tipo, acertou, usou_dica,"
            " n_tentativa, segundos, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (questao_id, modulo_id, tipo, int(acertou), int(usou_dica),
             n_tentativa, int(segundos), _hoje()),
        )
    return n_tentativa


def primeira_tentativa(questao_id):
    """A tentativa que conta, ou None se a questão ainda não foi respondida.

    É por aqui que a tela decide abrir a questão em modo leitura.
    """
    with conexao() as con:
        return con.execute(
            "SELECT * FROM tentativas WHERE questao_id = ? AND n_tentativa = 1",
            (questao_id,),
        ).fetchone()


# Acerto limpo vale 1, acerto com dica vale 0,5, erro vale 0.
_SOMA_DOS_PESOS = ("SUM(CASE WHEN acertou = 1 AND usou_dica = 0 THEN 1.0"
                   "         WHEN acertou = 1 AND usou_dica = 1 THEN 0.5"
                   "         ELSE 0 END)")


def dominio_modulo(modulo_id, total_questoes):
    """(acertos de 1ª sem dica + 0,5 × acertos de 1ª com dica) ÷ total do módulo.

    Esta é a métrica de progresso: mede o quanto do módulo já foi dominado, e
    por isso divide pelo módulo inteiro. Revisões do SRS (n_tentativa > 1) não
    entram na conta — elas mexem na retenção, não no domínio.
    """
    if not total_questoes:
        return 0.0
    with conexao() as con:
        pontos = con.execute(
            f"SELECT {_SOMA_DOS_PESOS} FROM tentativas"
            " WHERE modulo_id = ? AND n_tentativa = 1",
            (modulo_id,),
        ).fetchone()[0] or 0.0
    return min(pontos / total_questoes, 1.0)


def dominio_sobre_vistas(modulo_id):
    """Mesma soma de pesos, dividida só pelas questões que já foram vistas.

    Esta é a métrica de desempenho, e não de progresso: responde "como você vai
    indo no que já fez", sem penalizar quem simplesmente ainda não chegou no
    resto do módulo. É o que decide se um módulo está fraco.
    """
    with conexao() as con:
        linha = con.execute(
            f"SELECT {_SOMA_DOS_PESOS} AS pontos, COUNT(*) AS vistas FROM tentativas"
            " WHERE modulo_id = ? AND n_tentativa = 1",
            (modulo_id,),
        ).fetchone()
    if not linha["vistas"]:
        return 0.0
    return (linha["pontos"] or 0.0) / linha["vistas"]


def questoes_vistas(modulo_id):
    """Ids das questões do módulo que já receberam uma primeira tentativa."""
    with conexao() as con:
        linhas = con.execute(
            "SELECT questao_id FROM tentativas WHERE modulo_id = ? AND n_tentativa = 1",
            (modulo_id,),
        ).fetchall()
    return {linha["questao_id"] for linha in linhas}


def primeiras_tentativas(modulo_id=None):
    """As tentativas que contam. Sem argumento, as de todos os módulos."""
    sql = "SELECT * FROM tentativas WHERE n_tentativa = 1"
    parametros = ()
    if modulo_id is not None:
        sql += " AND modulo_id = ?"
        parametros = (modulo_id,)
    with conexao() as con:
        return con.execute(sql + " ORDER BY id", parametros).fetchall()


def ultimas_primeiras_tentativas(limite):
    """As `limite` primeiras tentativas mais recentes, da mais nova para a mais velha.

    É o que alimenta o ajuste de dificuldade das questões novas.
    """
    with conexao() as con:
        return con.execute(
            "SELECT * FROM tentativas WHERE n_tentativa = 1 ORDER BY id DESC LIMIT ?",
            (limite,),
        ).fetchall()


# --- repetição espaçada -----------------------------------------------------

def srs_obter(questao_id):
    with conexao() as con:
        return con.execute("SELECT * FROM srs WHERE questao_id = ?", (questao_id,)).fetchone()


def srs_salvar(questao_id, modulo_id, intervalo, facilidade, proxima_data, acertos, erros):
    with conexao() as con:
        con.execute(
            "INSERT INTO srs (questao_id, modulo_id, intervalo, facilidade, proxima_data,"
            " acertos, erros) VALUES (?, ?, ?, ?, ?, ?, ?)"
            " ON CONFLICT(questao_id) DO UPDATE SET"
            " intervalo = excluded.intervalo, facilidade = excluded.facilidade,"
            " proxima_data = excluded.proxima_data, acertos = excluded.acertos,"
            " erros = excluded.erros",
            (questao_id, modulo_id, intervalo, facilidade, proxima_data, acertos, erros),
        )


def srs_vencidos(data):
    """Questões com revisão vencida até a data (ISO 8601), da mais atrasada em diante."""
    with conexao() as con:
        return con.execute(
            "SELECT questao_id, modulo_id FROM srs WHERE proxima_data <= ?"
            " ORDER BY proxima_data, questao_id",
            (data,),
        ).fetchall()


def srs_do_modulo(modulo_id):
    with conexao() as con:
        return con.execute("SELECT * FROM srs WHERE modulo_id = ?", (modulo_id,)).fetchall()


# --- status dos módulos -----------------------------------------------------

def salvar_status_modulo(modulo_id, desbloqueado, concluido, dominio):
    with conexao() as con:
        con.execute(
            "INSERT INTO modulos_status (modulo_id, desbloqueado, concluido, dominio,"
            " atualizado_em) VALUES (?, ?, ?, ?, ?)"
            " ON CONFLICT(modulo_id) DO UPDATE SET"
            " desbloqueado = excluded.desbloqueado, concluido = excluded.concluido,"
            " dominio = excluded.dominio, atualizado_em = excluded.atualizado_em",
            (modulo_id, int(desbloqueado), int(concluido), float(dominio), _hoje()),
        )


def status_modulos():
    with conexao() as con:
        linhas = con.execute("SELECT * FROM modulos_status").fetchall()
    return {linha["modulo_id"]: linha for linha in linhas}


def apagar_tentativas_modulo(modulo_id):
    """"Refazer módulo do zero": a única forma de melhorar um domínio ruim.

    Apaga as tentativas e o estado de SRS do módulo. Quem chama é responsável
    por avisar o usuário de que a estatística será zerada.
    """
    with conexao() as con:
        con.execute("DELETE FROM tentativas WHERE modulo_id = ?", (modulo_id,))
        con.execute("DELETE FROM srs WHERE modulo_id = ?", (modulo_id,))
        con.execute(
            "UPDATE modulos_status SET concluido = 0, dominio = 0, atualizado_em = ?"
            " WHERE modulo_id = ?",
            (_hoje(), modulo_id),
        )
