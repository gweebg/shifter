import 'package:flutter/material.dart';

import 'navbar/navbar.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Shifter',
      theme: ThemeData(primarySwatch: Colors.amber,),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget
{
  const MyHomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context)
  {
    return Scaffold(
      body: Container(
          child: Column(
            children: <Widget>[
              Navbar()
            ],
        ),
      )
    );
  }
}

