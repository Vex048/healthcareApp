import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'package:healthcare_frontend/routing/app_router.dart';
import 'package:shared_preferences/shared_preferences.dart';

// Router provider na
final routerProvider = Provider<GoRouter>((ref) {
  final isLoggedInAsync = ref.watch(authStateFutureProvider);
  return buildGoRouter(isLoggedInAsync);
});

final authStateFutureProvider = FutureProvider<bool>((ref) async {
  final prefs = await SharedPreferences.getInstance();
  final token = prefs.getString('auth_token');
  return token != null;
});
