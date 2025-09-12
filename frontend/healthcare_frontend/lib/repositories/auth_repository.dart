import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:healthcare_frontend/infrastructure/api/api_client.dart';

import 'package:healthcare_frontend/utils/logger.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthRepository {
  AuthRepository({required this.apiClient});
  final ApiClient apiClient;

  // Trzba zrobić register dla użytkownika i na jego podstawie pacjenta
  Future<bool> registerUser({
    required String email, // username is used as email
    required String password1,
    required String password2,
    required String firstName,
    required String lastName,
  }) async {
    try {
      await apiClient.register({
        'email': email,
        'password1': password1,
        'password2': password2,
        'first_name': firstName,
        'last_name': lastName,
      });
      return true;
    } catch (e) {
      logger.e("Registration failed: $e");
      return false;
    }
  }

  Future<bool> login({required String email, required String password}) async {
    try {
      final response = await apiClient.login({
        'email': email,
        'password': password,
      });
      if (response.containsKey('key')) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('auth_token', response['key']);

        final user = await apiClient.getCurrentUser();
        await prefs.setString('user_data', jsonEncode(user));

        return true;
      } else {
        return false;
      }
    } catch (e) {
      logger.e("Login failed: $e");
      return false;
    }
  }

  Future<void> logout() async {
    return apiClient.logout();
  }

  Future<void> authStateChanges() async {
    throw UnimplementedError();
  }
}
