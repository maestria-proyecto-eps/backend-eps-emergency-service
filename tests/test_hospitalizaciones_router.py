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