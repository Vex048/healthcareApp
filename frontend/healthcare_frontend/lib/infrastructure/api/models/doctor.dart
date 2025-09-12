import 'package:freezed_annotation/freezed_annotation.dart';

@freezed
abstract class Doctor with _$Doctor {
  const factory Doctor({
    required String id,
    required int user,
    required String firstName,
    String secondName,
    required String lastName,
    required String email,
  }) = _Doctor;

  factory Doctor.fromJson(Map<String, dynamic> json) => _$DoctorFromJson(json);
}
