

import 'package:freezed_annotation/freezed_annotation.dart';

@freezed
abstract class Patient with _$Patient {
  const factory Patient({
    required int id,
    required int user,
    required int pesel;
  }) = _Patient;
  factory Patient.fromJson(Map<String, dynamic> json) => _$PatientFromJson(json);