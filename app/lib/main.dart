import 'package:flutter/material.dart';
import 'package:shifter/views/home/home_view.dart';

void main() => runApp(Shifter());

class Shifter extends StatelessWidget {

  const Shifter({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {

    return MaterialApp(
      title: 'Shifter',
      theme: ThemeData(primarySwatch: Colors.deepPurple),
      home: HomeView()
    );

  }
}
