def test_crear_hospitalizacion_urgencia_no_existe(client):
    response = client.post("/api/hospitalizacion", json={
        "id_urgencia":999
    })
    assert response.status_code == 400
    assert response.json()["message"] == "La atención de urgencias no existe"

def test_crear_hospitalizacion_atencion_ya_existe(client,crear_urgencia,crear_hospitalizacion):

    urgencia = crear_urgencia
    hospitalziacion= crear_hospitalizacion

    response = client.post("/api/hospitalizacion", json={
        "id_urgencia":urgencia.id_urgencia
    })
    assert response.status_code == 400
    assert response.json()["message"] == "Ya existe una hospitalización para esta atención de urgencias"

def test_crear_hospitalizacion_exitoso(client,borrar_hospitalizaciones):
    #Toca borrar las hospitalizaciones para que no exista una hospitalización previa a la urgencia con id 50
    response = client.post("/api/hospitalizacion", json={
        "id_urgencia":50
    })
    assert response.status_code == 201
    assert response.json()["data"]["id_urgencia"] == 50

def test_crear_atencion_hospitalizacion_doctor_no_existe(client, crear_hospitalizacion):
    response = client.post("/api/hospitalizacion/atencion", json={
        "id_doctor": 99999,
        "id_diagnostico": 1,
        "id_hospitalizacion": crear_hospitalizacion.id_hospitalizacion,
        "observaciones": "Observaciones de prueba",
        "tratamiento": "Tratamiento de prueba"
    })
    assert response.status_code == 400
    assert response.json()["message"] == "El doctor no existe"

def test_crear_atencion_hospitalizacion_diagnostico_no_existe(client, crear_hospitalizacion, crear_doctor):
    response = client.post("/api/hospitalizacion/atencion", json={
        "id_doctor": 12345,
        "id_diagnostico": 999,
        "id_hospitalizacion": crear_hospitalizacion.id_hospitalizacion,
        "observaciones": "Observaciones de prueba",
        "tratamiento": "Tratamiento de prueba"
    })
    assert response.status_code == 400
    assert response.json()["message"] == "El diagnóstico no existe"

def test_crear_atencion_hospitalizacion_hospitalizacion_no_existe(client, crear_doctor, crear_diagnostico):
    response = client.post("/api/hospitalizacion/atencion", json={
        "id_doctor": 12345,
        "id_diagnostico": 1,
        "id_hospitalizacion": 999,
        "observaciones": "Observaciones de prueba",
        "tratamiento": "Tratamiento de prueba"
    })
    assert response.status_code == 400
    assert response.json()["message"] == "La hospitalización no existe"

def test_crear_atencion_hospitalizacion_exitoso(client, crear_hospitalizacion, crear_doctor, crear_diagnostico):
    response = client.post("/api/hospitalizacion/atencion", json={
        "id_doctor": 12345,
        "id_diagnostico": 1,
        "id_hospitalizacion": crear_hospitalizacion.id_hospitalizacion,
        "observaciones": "Observaciones de prueba",
        "tratamiento": "Tratamiento de prueba"
    })
    assert response.status_code == 201
    assert response.json()["data"]["id_doctor"] == 12345
    assert response.json()["data"]["id_diagnostico"] == 1
    assert response.json()["data"]["id_hospitalizacion"] == crear_hospitalizacion.id_hospitalizacion

def test_obtener_atenciones_hospitalizacion_no_existe(client):
    response = client.get("/api/hospitalizacion/atencion/999")
    assert response.status_code == 400
    assert response.json()["message"] == "La hospitalización no existe"

def test_obtener_atenciones_hospitalizacion_exitoso(client, crear_hospitalizacion, crear_atencion_hospitalizacion):
    response = client.get(f"/api/hospitalizacion/atencion/{crear_hospitalizacion.id_hospitalizacion}")
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]) > 0




def test_ingreso_hospitalizacion_no_existe(client):
    response = client.put("/api/hospitalizacion/ingreso/999", json={
        "num_cama": 10
    })
    assert response.status_code == 400
    assert response.json()["message"] == "La hospitalización no existe"


def test_ingreso_hospitalizacion_ya_ingresada(client, crear_hospitalizacion):
    client.put(f"/api/hospitalizacion/ingreso/{crear_hospitalizacion.id_hospitalizacion}", json={
        "num_cama": 10
    })
    response = client.put(f"/api/hospitalizacion/ingreso/{crear_hospitalizacion.id_hospitalizacion}", json={
        "num_cama": 10
    })
    assert response.status_code == 400
    assert response.json()["message"] == "La hospitalización ya fue ingresada o dada de salida"


def test_ingreso_hospitalizacion_exitoso(client, borrar_hospitalizaciones, crear_urgencia):
    res_crear = client.post("/api/hospitalizacion", json={"id_urgencia": crear_urgencia.id_urgencia})
    assert res_crear.status_code == 201
    id_hosp = res_crear.json()["data"]["id_hospitalizacion"]

    response = client.put(f"/api/hospitalizacion/ingreso/{id_hosp}", json={
        "num_cama": 15
    })
    assert response.status_code == 200
    assert response.json()["data"]["estado"] == 1
    assert response.json()["data"]["num_cama"] == 15
    assert response.json()["data"]["ingreso"] is not None


def test_salida_hospitalizacion_no_existe(client):
    response = client.put("/api/hospitalizacion/salida/999")
    assert response.status_code == 400
    assert response.json()["message"] == "La hospitalización no existe"


def test_salida_hospitalizacion_no_ingresada(client, borrar_hospitalizaciones, crear_urgencia):
    res_crear = client.post("/api/hospitalizacion", json={"id_urgencia": crear_urgencia.id_urgencia})
    id_hosp = res_crear.json()["data"]["id_hospitalizacion"]

    response = client.put(f"/api/hospitalizacion/salida/{id_hosp}")
    assert response.status_code == 400
    assert response.json()["message"] == "La hospitalización no está en estado ingresado"


def test_salida_hospitalizacion_exitosa(client, borrar_hospitalizaciones, crear_urgencia):
    res_crear = client.post("/api/hospitalizacion", json={"id_urgencia": crear_urgencia.id_urgencia})
    id_hosp = res_crear.json()["data"]["id_hospitalizacion"]

    client.put(f"/api/hospitalizacion/ingreso/{id_hosp}", json={"num_cama": 20})

    response = client.put(f"/api/hospitalizacion/salida/{id_hosp}")
    assert response.status_code == 200
    assert response.json()["data"]["estado"] == 2
    assert response.json()["data"]["salida"] is not None


def test_listar_hospitalizaciones_vacio(client, borrar_hospitalizaciones):
    response = client.get("/api/hospitalizacion/")
    assert response.status_code == 200
    assert response.json()["data"]["hasElements"] is False


def test_listar_hospitalizaciones_exitoso(client, crear_hospitalizacion):
    response = client.get("/api/hospitalizacion/")
    assert response.status_code == 200
    assert response.json()["data"]["hasElements"] is True
    assert len(response.json()["data"]["data"]) > 0


def test_listar_hospitalizaciones_filtro_num_cama(client, crear_hospitalizacion):
    response = client.get("/api/hospitalizacion/?num_cama=101")
    assert response.status_code == 200
    for item in response.json()["data"]["data"]:
        assert item["num_cama"] == 101


def test_listar_hospitalizaciones_filtro_estado(client, crear_hospitalizacion):
    response = client.get("/api/hospitalizacion/?estado=0")
    assert response.status_code == 200
    for item in response.json()["data"]["data"]:
        assert item["estado"] == 0


def test_listar_hospitalizaciones_paginacion(client, crear_hospitalizacion):
    response = client.get("/api/hospitalizacion/?pag=1&cantidad=1")
    assert response.status_code == 200
    assert response.json()["data"]["page"] == 1
    assert len(response.json()["data"]["data"]) <= 1