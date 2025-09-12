import 'package:flutter/foundation.dart';
import 'package:healthcare_frontend/infrastructure/api/models/user.dart';

class UserProvider with ChangeNotifier {
  User? _user;

  User? get user => _user;

  bool get isDoctor => _user?.userType == 'doctor';
  bool get isPatient => _user?.userType == 'patient';

  void setUser(User user) {
    _user = user;
    notifyListeners();
  }

  void clearUser() {
    _user = null;
    notifyListeners();
  }
}
