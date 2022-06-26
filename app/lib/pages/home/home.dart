import 'package:flutter/material.dart';
import 'package:shifter/helpers/responsive.dart';
import 'package:shifter/pages/home/widgets/desktop.dart';
import 'package:shifter/pages/home/widgets/mobile.dart';
import '../../widgets/navbar_desktop.dart';

class HomeScreen extends StatelessWidget {

  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey();

  @override
  Widget build(BuildContext context) {

    Size screenSize = MediaQuery.of(context).size;

    return Scaffold(
      key: scaffoldKey,
      extendBodyBehindAppBar: true,
      appBar: PreferredSize(preferredSize: Size(screenSize.width, 1000), child: NavBar()),
      // appBar: ResponsiveWidget.isSmallScreen(context) ? mobileNavBar() : PreferredSize(preferredSize: Size(screenSize.width, 1000), child: NavBar())
      backgroundColor: Colors.white,
      body: ResponsiveWidget(largeScreen: DesktopScreen(), mediumScreen: DesktopScreen(), smallScreen: MobileScreen())
    );
  }
}
