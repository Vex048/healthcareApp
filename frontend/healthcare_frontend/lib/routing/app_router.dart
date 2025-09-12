import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:healthcare_frontend/infrastructure/api/models/user.dart';
import 'package:healthcare_frontend/interface/screens/auth/login_screen.dart';
import 'package:healthcare_frontend/interface/screens/auth/register_screen.dart';
import 'package:healthcare_frontend/interface/screens/home/home_screen.dart';

class Routes {
  Routes();
  static String homePage = '/';
  static String galleryPage = '/gallery';
  static String fetchDataPage = '/fetch-data';
  static String loginPage = '/login';
  static String registerPage = '/register';
  static String splashScreen = '/splash';
  static String profilePage = '/profile';
  static String singOut = '/logout';
}

GoRouter buildGoRouter(AsyncValue<bool?> authState) {
  return GoRouter(
    redirect: (context, state) {
      return authState.when(
        data: (isLoggedIn) {
          final isAuthPage =
              state.matchedLocation == Routes.loginPage ||
              state.matchedLocation == Routes.registerPage;
          if (isLoggedIn == true) {
            return isAuthPage ? Routes.homePage : null;
          } else {
            return state.matchedLocation == Routes.registerPage
                ? null
                : Routes.registerPage;
          }
        },
        loading: () => Routes.splashScreen,
        error: (_, __) => Routes.registerPage,
      );
    },
    routes: [
      GoRoute(path: Routes.homePage, builder: (context, state) => HomeScreen()),

      GoRoute(
        path: Routes.loginPage,
        builder: (context, state) => const LoginScreen(),
      ),

      GoRoute(
        path: Routes.registerPage,
        builder: (context, state) => const RegisterScreen(),
      ),

      GoRoute(
        path: Routes.splashScreen,
        builder: (context, state) =>
            const Scaffold(body: Center(child: CircularProgressIndicator())),
      ),
      // GoRoute(
      //   path: Routes.profilePage,
      //   builder: (context, state) => ProfilePage(),
      // ),
      // GoRoute(
      //   path: Routes.resetPasswordPage,
      //   builder: (context, state) => ResetPasswordPage(),
      // ),
      // GoRoute(
      //   path: Routes.singOut,
      //   builder: (context, state) => const LoginPage(),
      // ),
    ],
  );
}
