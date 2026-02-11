from flask import Flask, request, jsonify  # SEMPRE assim
from flask_cors import CORS
import oracledb

app = Flask(__name__)
CORS(app)
# ... restante do código do Oracle ...

app = Flask(__name__)
CORS(app) # Permite que o formulário aceda à API

# Configuração Oracle (Igual ao teu código)
oracledb.init_oracle_client(lib_dir=r"C:\Oracle\instantclient_23_0")
dsn = oracledb.makedsn(host="dbconnect.megaerp.online", port=4221, service_name="xepdb1")

def buscar_nomes_oracle(termo):
    conn = oracledb.connect(user="EZTEC", password="pseiz9i3UM", dsn=dsn)
    cursor = conn.cursor()
    
    # Busca nomes que contenham o que o usuário digitou (case insensitive)
    query = """
    SELECT NOMCCU FROM EZTEC_11081_RHP.R018ccu@EZTEC 
    WHERE UPPER(NOMCCU) LIKE UPPER(:termo)
    GROUP BY NOMCCU
    FETCH FIRST 10 ROWS ONLY
    """
    cursor.execute(query, termo=f"%{termo}%")
    resultados = [row[0] for row in cursor]
    
    cursor.close()
    conn.close()
    return resultados

@app.route('/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('q', '')
    if len(termo) < 3: # Só busca se tiver 3 ou mais letras para poupar o banco
        return jsonify([])
    
    nomes = buscar_nomes_oracle(termo)
    return jsonify(nomes)

if __name__ == '__main__':
    app.run(port=5000) # O servidor vai rodar em http://localhost:5000
