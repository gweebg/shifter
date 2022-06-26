import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'custom_button.dart';
import '../helpers/style.dart';

class NavBar extends StatefulWidget {
  const NavBar({Key? key}) : super(key: key);

  @override
  State<NavBar> createState() => _NavBarState();
}

class _NavBarState extends State<NavBar> {

  final List<bool> _isHovering = [false, false];

  @override
  Widget build(BuildContext context) {

    Size screenSize = MediaQuery.of(context).size;

    return PreferredSize(
      preferredSize: Size(screenSize.width, 1000),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 56, horizontal: 64),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget> [

            const Icon(Icons.school, size: 50),
            const SizedBox(width: 20),
            Text("Shifter", style: GoogleFonts.poppins(fontSize: 36, color: const Color.fromRGBO(87, 74, 74, 1.0))),

            Expanded(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: <Widget> [
                  SizedBox(width: screenSize.width / 8),
                  InkWell(
                    onHover: (value) {
                      setState(() {
                        value ?
                        _isHovering[0] = true :
                        _isHovering[0] = false;
                      });
                    },
                    hoverColor: Colors.transparent,
                    highlightColor: Colors.transparent,
                    splashColor: Colors.transparent,
                    onTap: () {}, /* TODO: Adicionar _launchURL(...) */
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: <Widget> [

                        const SizedBox(height: 12),
                        Wrap(
                          crossAxisAlignment: WrapCrossAlignment.center,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.schedule),
                              color: _isHovering[0] ? fadePurple : Colors.black,
                              onPressed: (){},
                              hoverColor: Colors.transparent,
                              highlightColor: Colors.transparent,
                              splashColor: Colors.transparent,),

                            Text("Schedules" , style: GoogleFonts.poppins(fontSize: 20, color: _isHovering[0] ? fadePurple : Colors.black, fontWeight: FontWeight.w400))
                          ],
                        ),

                      ],

                    )
                  ),

                  SizedBox(width: screenSize.width / 20),

                  InkWell(
                      onHover: (value) {
                        setState(() {
                          value ?
                          _isHovering[1] = true :
                          _isHovering[1] = false;
                        });
                      },
                      hoverColor: Colors.transparent,
                      highlightColor: Colors.transparent,
                      splashColor: Colors.transparent,
                      onTap: () {}, /* TODO: Adicionar _launchURL(...) */
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: <Widget> [

                          const SizedBox(height: 12),
                          //Text("Github" , style: GoogleFonts.poppins(fontSize: 20, color: _isHovering[1] ? fadePurple : Colors.black, fontWeight: FontWeight.w400)),
                          Wrap(
                            crossAxisAlignment: WrapCrossAlignment.center,
                            children: [
                              IconButton(
                                icon: const Icon(Icons.code),
                                color: _isHovering[1] ? fadePurple : Colors.black,
                                onPressed: (){},
                                hoverColor: Colors.transparent,
                                highlightColor: Colors.transparent,
                                splashColor: Colors.transparent,),

                              Text("Github" , style: GoogleFonts.poppins(fontSize: 20, color: _isHovering[1] ? fadePurple : Colors.black, fontWeight: FontWeight.w400))
                            ],
                          ),

                        ],

                      )
                  ),



                ],
              )
            )
          ],
        )
      )
    );
  }
}
