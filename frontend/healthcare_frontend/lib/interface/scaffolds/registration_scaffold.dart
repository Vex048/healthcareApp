import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class RegistrationScaffold extends ConsumerWidget {
  const RegistrationScaffold({
    super.key,
    required this.title,
    required this.body,
  });
  final String title;
  final Widget body;
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: body,
    );
  }
}
