import 'package:flutter/material.dart';
import 'package:park_finder/login_page.dart';
import 'package:park_finder/main_page.dart';
import 'package:park_finder/welcome/welcome_screen.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Parkfinder',
      home: WelcomeScreen(),
      routes: <String, WidgetBuilder>{
        '/login': (BuildContext context) => new LoginPage(),
        '/mainpage': (BuildContext context) => new MainPage(),
      },
    );
  }
}
