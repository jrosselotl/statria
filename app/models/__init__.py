# app/models/__init__.py

# Base “maestras”
from .company import Company
from .user import User
from .project import Project
from .user_project import UserProject

# Catálogos y jerarquías
from .specialty import Specialty
from .test_type import TestType

from .equipment_type import EquipmentType
from .equipment import Equipment
from .location import Location

# Certificados
from .quality_certificate import QualityCertificate
from .certificate_assignment import CertificateAssignment

# Asignaciones de pruebas a proyecto y ejecuciones
from .test_project import TestProject
from .test_run import TestRun

# Resultados (todas las variantes que tienes en /models)
from .test_result_mapping import TestResultMapping
from .test_result_continuity import TestResultContinuity
from .test_result_insulation import TestResultInsulation
from .test_result_contact_resistance import TestResultContactResistance
from .test_result_torque import TestResultTorque
