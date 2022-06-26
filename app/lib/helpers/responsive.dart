import 'package:flutter/material.dart';
import 'constants.dart';

class ResponsiveWidget extends StatelessWidget {

  final Widget largeScreen;
  final Widget mediumScreen;
  final Widget smallScreen;

  const ResponsiveWidget({Key? key, required this.largeScreen, required this.mediumScreen, required this.smallScreen}) : super(key: key);

  static bool isSmallScreen(BuildContext context) {
    return MediaQuery.of(context).size.width < smallScreenWidth;
  }

  static bool isMediumScreen(BuildContext context) {
    return MediaQuery.of(context).size.width >= smallScreenWidth && MediaQuery.of(context).size.width <= smallScreenWidth;
  }

  static bool isLargeScreen(BuildContext context) {
    return MediaQuery.of(context).size.width > smallScreenWidth;
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (context, constraints) {

      if (constraints.maxWidth > largeScreenWidth) {
        return largeScreen;
      } else if (constraints.maxWidth >= smallScreenWidth && constraints.maxWidth < largeScreenWidth) {
        return mediumScreen;
      } else {
        return smallScreen;
      }

    });
  }

}

