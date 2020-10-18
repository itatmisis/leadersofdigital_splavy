import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/io_client.dart';

var url = 'http://78.47.20.210:8000/auth/jwt/login';
bool trustSelfSigned = true;
HttpClient httpClient = new HttpClient()
  ..badCertificateCallback =
      ((X509Certificate cert, String host, int port) => trustSelfSigned);
IOClient ioClient = new IOClient(httpClient);

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  @override
  Widget build(BuildContext context) {
    TextEditingController loginUsernameController = TextEditingController();
    TextEditingController loginPasswordController = TextEditingController();

    double width = MediaQuery.of(context).size.width;
    double height = MediaQuery.of(context).size.height;
    return Scaffold(
      body: Center(
          child: Container(
        height: height,
        width: width * 0.85,
        child: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: width / 2,
                height: height / 2,
                child: Image.asset(
                  "assets/logo.jpeg",
                  fit: BoxFit.fitWidth,
                  width: 220.0,
                  alignment: Alignment.center,
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(0.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('Parkfinder',
                        style: TextStyle(
                            fontSize: 25.0, fontWeight: FontWeight.bold),
                        textAlign: TextAlign.center),
                  ],
                ),
              ),
              SizedBox(
                height: 30.0,
              ),
              TextField(
                controller: loginUsernameController,
                decoration: InputDecoration(
                  hintText: 'Почта',
                  suffixIcon: Icon(Icons.email),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(20.0),
                  ),
                ),
              ),
              SizedBox(
                height: 20.0,
              ),
              TextField(
                controller: loginPasswordController,
                obscureText: true,
                decoration: InputDecoration(
                  hintText: 'Пароль',
                  suffixIcon: Icon(Icons.lock),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(20.0),
                  ),
                ),
              ),
              SizedBox(
                height: 30.0,
              ),
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Builder(
                      builder: (ctx) => RaisedButton(
                        child: Text(
                          'Войти',
                          style: TextStyle(color: Colors.white),
                        ),
                        color: Color(0xFF6C63FF),
                        onPressed: () {
                          (() async {
                            Map<String, dynamic> body = {
                              "username": loginUsernameController.text,
                              "password": loginPasswordController.text,
                            };
                            var headers = {
                              'Content-Type':
                                  'application/x-www-form-urlencoded',
                            };
                            var result = await ioClient.post(url,
                                headers: headers, body: body);
                            if (result.statusCode == 200)
                              Navigator.of(ctx).pushNamed("/mainpage");
                            else
                              print(result.statusCode);
                          })();
                        },
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      )),
    );
  }
}
