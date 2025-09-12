import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:healthcare_frontend/providers/api_providers.dart';
import 'package:healthcare_frontend/repositories/auth_repository.dart';

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return AuthRepository(apiClient: apiClient);
});
