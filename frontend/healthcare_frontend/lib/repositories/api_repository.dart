import 'package:healthcare_frontend/infrastructure/api/api_client.dart';
import 'package:healthcare_frontend/infrastructure/api/models/doctor.dart';
import 'package:healthcare_frontend/infrastructure/api/models/patient.dart';

class ApiRepository {
  final ApiClient apiClient;

  ApiRepository(this.apiClient);

  Future<List<Doctor>> getDoctors() async {
    return apiClient.getDoctors();
  }

  // Jeżeli użytkownik to pacjent to powinno to zwrócić jego profil
  // A jeżeli doktor to profile jego pacjentów?
  Future<List<Patient>> getPatients() async {
    return apiClient.getPatientProfile();
  }

  Future<List<Doctor>> getDoctorProfile(int id) async {
    // Implementacja pobierania profilu doktora po ID
    throw UnimplementedError();
  }
}
