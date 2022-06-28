import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class NavbarItemButton extends StatelessWidget {

  final String text;

  const NavbarItemButton({Key? key, required this.text}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Text(text, style: GoogleFonts.poppins(fontSize: 20, color: const Color.fromRGBO(87, 74, 74, 1.0)));
  }
}

