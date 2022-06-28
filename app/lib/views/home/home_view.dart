import 'package:flutter/material.dart';
import 'package:shifter/widgets/centered_view/centered_view.dart';
import 'package:shifter/widgets/navbar/navbar_desktop.dart';

import '../../helpers/colors.dart';
import '../../widgets/form/form.dart';

class HomeView extends StatelessWidget {
  const HomeView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(

      decoration: const BoxDecoration(
        image: DecorationImage(image: AssetImage("assets/images/background.png"), fit: BoxFit.fill),
      ),

      child: Scaffold(
        backgroundColor: Colors.transparent,
        body: CenteredView(
          child: Column(
            children: [NavbarDesktop(), const SizedBox(height: 40), ShifterForm()],
          ),
        )

      ),
    );
  }
}
