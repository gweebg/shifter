import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:url_launcher/url_launcher_string.dart';

class Navbar extends StatelessWidget {
  const Navbar({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth > 1200) {
            return DesktopNavbar();
        }
        else if (constraints.maxWidth > 800 && constraints.maxWidth < 1200) {
          return TabletNavBar(); //TabletNavBar();
        }
        else {
          return MobileNavbar(); //MobileNavbar();
        }
      },
    );
  }
}

class DesktopNavbar extends StatelessWidget {
  const DesktopNavbar({Key? key}) : super(key: key);

  Future<void> _launchInBrowser(String url) async {
    if (!await launchUrlString(url, mode: LaunchMode.externalApplication)) {
      throw 'Could not launch $url';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 56, horizontal: 64),
      child: Container(
        constraints: const BoxConstraints(maxWidth: 1920),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: <Widget>[
            Wrap(
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                //Image.asset("assets/images/shifter_logo_better.png", scale: 15),
                const Icon(Icons.school, size: 50),
                const SizedBox(width: 20),
                Text("Shifter", style: GoogleFonts.poppins(fontSize: 36, color: const Color.fromRGBO(87, 74, 74, 1.0)))
              ],
            ),
            // Text("Shifter", style: GoogleFonts.poppins(fontSize: 36, color: const Color.fromRGBO(87, 74, 74, 1.0))),
            Row(
              children: <Widget>[

                FloatingActionButton.extended(
                  label: Text("Schedules"   , style: GoogleFonts.poppins(fontSize: 16, color: Colors.black, fontWeight: FontWeight.w400)),
                  backgroundColor: Colors.white,
                  onPressed: () {
                    const url = "https://alunos.uminho.pt/pt/estudantes/paginas/infouteishorarios.aspx";
                    _launchInBrowser(url);
                  },
                  icon: const Icon(Icons.schedule)
                ),
                const SizedBox(width: 48),

                FloatingActionButton.extended(
                  label: Text("Github"   , style: GoogleFonts.poppins(fontSize: 16, color: Colors.black, fontWeight: FontWeight.w400)),
                  backgroundColor: Colors.white,
                  onPressed: () {
                    const url = "https://github.com/gweebg/shifter";
                    _launchInBrowser(url);
                  },
                  icon: const Icon(Icons.code)
                ),
              ],
            ),

          ],
        ),
      ),
    );
  }
}

class TabletNavBar extends StatelessWidget {
  const TabletNavBar({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}

class MobileNavbar extends StatelessWidget {
  const MobileNavbar({Key? key}) : super(key: key);

  Future<void> _launchInBrowser(String url) async {
    if (!await launchUrlString(url, mode: LaunchMode.externalApplication)) {
      throw 'Could not launch $url';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 56, horizontal: 64),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        //crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Wrap(
                crossAxisAlignment: WrapCrossAlignment.center,
                children: [
                  //Image.asset("assets/images/shifter_logo_better.png", scale: 15),
                  const Icon(Icons.school, size: 50),
                  const SizedBox(width: 20),
                  Text("Shifter", style: GoogleFonts.poppins(fontSize: 36, color: const Color.fromRGBO(87, 74, 74, 1.0)))
                ],
              ),
            ],
          ),
          SizedBox(height: 20),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              FloatingActionButton.extended(
                  label: Text("Schedules"   , style: GoogleFonts.poppins(fontSize: 16, color: Colors.black, fontWeight: FontWeight.w400)),
                  backgroundColor: Colors.white,
                  onPressed: () {
                    const url = "https://alunos.uminho.pt/pt/estudantes/paginas/infouteishorarios.aspx";
                    _launchInBrowser(url);
                  },
                  icon: const Icon(Icons.schedule)
              ),
              const SizedBox(width: 48),

              FloatingActionButton.extended(
                  label: Text("Github"   , style: GoogleFonts.poppins(fontSize: 16, color: Colors.black, fontWeight: FontWeight.w400)),
                  backgroundColor: Colors.white,
                  onPressed: () {
                    const url = "https://github.com/gweebg/shifter";
                    _launchInBrowser(url);
                  },
                  icon: const Icon(Icons.code)
              ),
            ],
          )
        ],
      ),
    );
  }
}


