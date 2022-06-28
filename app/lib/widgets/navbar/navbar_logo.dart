import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class NavbarLogo extends StatelessWidget {

  const NavbarLogo({Key? key}) : super(key: key);

  // const Icon(Icons.school, size: 50),
  // const SizedBox(width: 20),
  // Text("Shifter", style: GoogleFonts.poppins(fontSize: 36, color: const Color.fromRGBO(87, 74, 74, 1.0))),

  @override
  Widget build(BuildContext context) {
    return Row(

      children: [
        const Icon(Icons.school, size: 50),
        const SizedBox(width: 20),
        Text("Shifter", style: GoogleFonts.poppins(fontSize: 36, color: const Color.fromRGBO(87, 74, 74, 1.0))),
      ],

    );
  }
}
