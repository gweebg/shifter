import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:shifter/widgets/main_form.dart';

import '../../../helpers/style.dart';

class DesktopScreen extends StatelessWidget {

  const DesktopScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {

    Size screenSize = MediaQuery.of(context).size;

    List<bool> options = [false, false];

    return Container(

      constraints: const BoxConstraints(maxWidth: 1440),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,

        children: <Widget> [

          Container(
            padding: const EdgeInsets.symmetric(horizontal: 80),
            width: screenSize.width / 2,
            child: MainFormScreen()
          ),

        ],

      )

    );
  }
}

/*
Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget> [

                Container(
                  alignment: Alignment.centerLeft,
                  margin: const EdgeInsets.only(bottom: 15),
                  child: Text("Select your course :" , style: GoogleFonts.poppins(fontSize: 24, color: text, fontWeight: FontWeight.w400))
                ),

                TextField(
                  decoration: InputDecoration(
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      filled: true,
                      hintStyle: GoogleFonts.poppins(fontSize: 14, color: Colors.grey, fontWeight: FontWeight.w400),
                      hintText: "Start typing to check every course available",
                      fillColor: Colors.white70
                  ),
                ),

                const SizedBox(height: 14),

                Container(
                    alignment: Alignment.centerLeft,
                    margin: const EdgeInsets.only(bottom: 15),
                    child: Text("Select a year :" , style: GoogleFonts.poppins(fontSize: 24, color: text, fontWeight: FontWeight.w400))
                ),

                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    SizedBox(
                      width: 60,
                      child: TextField(
                        decoration: InputDecoration(
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(10.0),
                            ),
                            filled: true,
                            hintStyle: GoogleFonts.poppins(fontSize: 14, color: Colors.grey, fontWeight: FontWeight.w400),
                            hintText: "Year",
                            fillColor: Colors.white70),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 14),

                Container(
                    alignment: Alignment.centerLeft,
                    margin: const EdgeInsets.only(bottom: 15),
                    child: Text("Select week date :" , style: GoogleFonts.poppins(fontSize: 24, color: text, fontWeight: FontWeight.w400))
                ),

                TextField(
                  decoration: InputDecoration(
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      filled: true,
                      hintStyle: GoogleFonts.poppins(fontSize: 14, color: Colors.grey, fontWeight: FontWeight.w400),
                      hintText: "Insert week date (dd-mm-YYYY)",
                      fillColor: Colors.white70),
                )
              ],
            ),
 */
