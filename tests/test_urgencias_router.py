import datetime

from models.AtencionUrgencias import AtencionUrgencias
from models.CatalogoDiagnosticos import CatalogoDiagnosticos
from models.Doctor import Doctor
from models.Triages import Triages


def test_crear_triage_exitoso(client):
    response = client.post("/api/triages", json={
        "id_paciente": 123456789,
        "motivo": "Dolor fuerte en el pecho",
        "nivel": 5,
        "id_enfermero": 111,
        "antecedentes": "Hipertensión",
        "alergias": "Ninguna",
        "hallazgos": "Paciente con dolor torácico",
        "medicamentos": "Losartán",
        "pulso": "90",
        "presion_arterial": "140/90",
        "frecuencia_cardiaca": "90",
        "frecuencia_respiratoria": "20",
        "temperatura": "37.2",
        "saturacion_oxigeno": "96",
        "escala_dolor": 8,
        "riesgo_vital": True
    })

    assert response.status_code == 201
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Triage creado exitosamente"
    assert body["data"]["id_paciente"] == 123456789
    assert body["data"]["estado"] == 0
    assert body["data"]["nivel"] == 5
    assert body["data"]["riesgo_vital"] is True
    assert body["data"]["fechat"] is not None


def test_listar_triages_exitoso(client):
    response = client.get("/api/triages")

    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Listado de triages"
    assert "data" in body
    assert isinstance(body["data"]["data"], list)


def test_obtener_primer_triage_pendiente(client, db_session):

    triage = Triages(
        id_paciente=222222222,
        motivo="Dificultad respiratoria",
        nivel=4,
        id_enfermero=111,
        antecedentes=None,
        fechat=datetime.datetime.now() - datetime.timedelta(minutes=20),
        estado=0,
        alergias=None,
        hallazgos="Paciente con dificultad respiratoria",
        medicamentos=None,
        pulso="100",
        presion_arterial="130/80",
        frecuencia_cardiaca="100",
        frecuencia_respiratoria="24",
        temperatura="37.0",
        saturacion_oxigeno="90",
        escala_dolor=6,
        riesgo_vital=True
    )
    db_session.add(triage)
    db_session.commit()
    db_session.refresh(triage)

    response = client.get("/api/triages/urgencia/first")

    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["data"]["estado"] == 0
    assert body["data"]["nivel"] >= 4

def test_atender_triage_exitoso(client, db_session):

    triage = Triages(
        id_paciente=333333333,
        motivo="Herida abierta",
        nivel=3,
        id_enfermero=111,
        antecedentes=None,
        fechat=datetime.datetime.now(),
        estado=0,
        alergias=None,
        hallazgos="Herida en brazo",
        medicamentos=None,
        pulso="80",
        presion_arterial="120/80",
        frecuencia_cardiaca="80",
        frecuencia_respiratoria="18",
        temperatura="36.8",
        saturacion_oxigeno="98",
        escala_dolor=5,
        riesgo_vital=False
    )
    db_session.add(triage)
    db_session.commit()
    db_session.refresh(triage)

    response = client.put(f"/api/triages/atender/{triage.id_triage}")

    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Triage atendido exitosamente"
    assert body["data"]["estado"] == 1

def test_atender_triage_ya_atendido(client, db_session):

    triage = Triages(
        id_paciente=444444444,
        motivo="Dolor abdominal",
        nivel=2,
        id_enfermero=111,
        antecedentes=None,
        fechat=datetime.datetime.now(),
        estado=1,
        alergias=None,
        hallazgos="Dolor moderado",
        medicamentos=None,
        pulso="75",
        presion_arterial="118/78",
        frecuencia_cardiaca="75",
        frecuencia_respiratoria="17",
        temperatura="36.7",
        saturacion_oxigeno="99",
        escala_dolor=4,
        riesgo_vital=False
    )
    db_session.add(triage)
    db_session.commit()
    db_session.refresh(triage)

    response = client.put(f"/api/triages/atender/{triage.id_triage}")

    assert response.status_code == 409
    body = response.json()
    assert body["hasError"] is True
    assert body["message"] == "El triage ya fue atendido"


def test_crear_atencion_urgencias_exitoso(client, db_session, db_admin_session):

    triage = Triages(
        id_paciente=555555555,
        motivo="Fiebre alta",
        nivel=3,
        id_enfermero=111,
        antecedentes=None,
        fechat=datetime.datetime.now(),
        estado=1,
        alergias=None,
        hallazgos="Paciente febril",
        medicamentos=None,
        pulso="95",
        presion_arterial="120/80",
        frecuencia_cardiaca="95",
        frecuencia_respiratoria="19",
        temperatura="39.0",
        saturacion_oxigeno="97",
        escala_dolor=3,
        riesgo_vital=False
    )
    db_session.add(triage)

    diagnostico = CatalogoDiagnosticos(
        id_diagnostico=99,
        nombre_enfermedad="Diagnóstico prueba"
    )
    db_session.add(diagnostico)

    doctor = Doctor(
        id_medico=54321,
        num_licencia=999999,
        id_especialidad=1
    )
    db_admin_session.add(doctor)

    db_session.commit()
    db_admin_session.commit()
    db_session.refresh(triage)

    response = client.post("/api/atencion_urgencias", json={
        "id_doctor": 54321,
        "observaciones": "Paciente atendido en urgencias",
        "tratamiento": "Tratamiento inicial",
        "id_triage": triage.id_triage,
        "id_diagnostico": 99
    })

    assert response.status_code == 201
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Atención de urgencias creada exitosamente"
    assert body["data"]["id_doctor"] == 54321
    assert body["data"]["id_triage"] == triage.id_triage
    assert body["data"]["id_diagnostico"] == 99


def test_listar_atenciones_urgencias_exitoso(client):
    response = client.get("/api/atencion_urgencias")

    assert response.status_code == 200
    body = response.json()
    assert body["hasError"] is False
    assert body["message"] == "Listado de atenciones de urgencias"
    assert "data" in body
    assert isinstance(body["data"]["data"], list)