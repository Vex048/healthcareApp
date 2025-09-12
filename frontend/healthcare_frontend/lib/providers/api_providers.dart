import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:healthcare_frontend/infrastructure/api/api_client.dart';
import 'package:healthcare_frontend/infrastructure/config/env_config.dart';
import 'package:shared_preferences/shared_preferences.dart';

final baseOptionsProvider = Provider<BaseOptions>(
  (ref) => BaseOptions(
    baseUrl: EnvConfig.apiBaseUrl,
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
    sendTimeout: const Duration(seconds: 10),
  ),
);

final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(ref.read(baseOptionsProvider));
  dio.interceptors.add(TokenInterceptor());
  return dio;
});

final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient(ref.watch(dioProvider));
});

class TokenInterceptor extends Interceptor {
  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('auth_token');

    if (token != null) {
      options.headers['Authorization'] = 'Token $token';
    }

    super.onRequest(options, handler);
  }
}
