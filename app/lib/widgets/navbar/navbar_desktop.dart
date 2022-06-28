import 'package:flutter/material.dart';

import 'navbar_item.dart';
import 'navbar_logo.dart';

class NavbarDesktop extends StatelessWidget {
  const NavbarDesktop({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
        color: Colors.amber,
        height: 100,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const NavbarLogo(),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                NavbarItemButton(text: "Schedules"),
                SizedBox(width: 60),
                NavbarItemButton(text: "Github")
              ],
            )
          ],
        ));
  }
}
