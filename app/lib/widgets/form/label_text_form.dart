import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../../helpers/colors.dart';

class LabelTextForm extends StatelessWidget {

  final String text;
  final double? fontSize;

  const LabelTextForm({Key? key, required this.text, required this.fontSize}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.centerLeft,
      margin: const EdgeInsets.only(bottom: 15),
      child: Text(text,
          style: GoogleFonts.poppins(
              fontSize: fontSize,
              color: colorText,
              fontWeight: FontWeight.w400)));
  }
}
