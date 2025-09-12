import 'package:dio/dio.dart';
import 'package:healthcare_frontend/infrastructure/api/models/doctor.dart';
import 'package:healthcare_frontend/infrastructure/api/models/patient.dart';
import 'package:healthcare_frontend/infrastructure/api/models/user.dart';
import 'package:retrofit/retrofit.dart';
part 'api_client.g.dart';

// The restAPI wil communicate with Django REST framework

@RestApi()
abstract class ApiClient {
  factory ApiClient(Dio dio, {String? baseUrl}) = _ApiClient;

  @POST("auth/login/")
  Future<Map<String, dynamic>> login(@Body() Map<String, dynamic> credentials);

  @POST("auth/registration/")
  Future<Map<String, dynamic>> register(@Body() Map<String, dynamic> userData);

  @POST('/auth/logout/')
  Future<void> logout();

  // I tutaj
  @GET("patients/profiles/")
  Future<List<Patient>> getPatientProfile();

  @GET("auth/user/")
  Future<User> getCurrentUser();

  @GET('/patients/records/')
  Future<List<MedicalRecord>> getPatientMedicalRecords();

  @GET('patients/records/{id}/')
  Future<void> getPatientRecords(@Path('id') int id);

  @GET('/doctors/profiles/{id}/')
  Future<void> getDoctorProfile(@Path('id') int id);

  @GET("doctors/profiles/")
  Future<List<Doctor>> getDoctors({@Query("search") String? searchQuery});

  // Czy ten endpoint wystarczy i dla pacjentow i doktorow?
  @GET("doctors/availability/")
  Future<List<Availability>> getAvailableSlots({
    @Query("doctor") int? doctorId,
  });

  @POST('doctors/availability/')
  Future<Availability> createAvailabilitySlot(
    @Body() Map<String, dynamic> data,
  );

  @PUT('doctors/availability/{id}/')
  Future<Availability> updateAvailabilitySlot(
    @Path('id') int id,
    @Body() Map<String, dynamic> data,
  );

  // Czy ten endpoint też może działac zarówno dla pacjentów jak i doktorów?
  @GET('doctors/appointments/')
  Future<List<Appointment>> getMyAppointments();

  // TO jest niby z jakimś filteringiem
  @GET("doctors/appointments/")
  Future<List<Appointment>> getAppointments({@Query("status") String? status});

  @POST("doctors/appointments/")
  Future<dynamic> createAppointment(
    @Body() Map<String, dynamic> appointmentData,
  );

  @POST("doctors/appointments/{id}/cancel/")
  Future<void> cancelAppointment(@Path() int id);
}
