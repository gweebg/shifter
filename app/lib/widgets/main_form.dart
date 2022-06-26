import 'package:checkbox_formfield/checkbox_formfield.dart';
import 'package:flutter/material.dart';
import 'package:flutter_typeahead/flutter_typeahead.dart';
import 'package:google_fonts/google_fonts.dart';

import '../helpers/style.dart';

class MainFormScreen extends StatefulWidget {
  const MainFormScreen({Key? key}) : super(key: key);

  @override
  State<MainFormScreen> createState() => _MainFormScreenState();
}

class _MainFormScreenState extends State<MainFormScreen> {

  String _courseName = "";
  String _courseYear = "";
  String _weekDate = "";

  bool _jsonOnly = false;
  bool _shiftFilter = true;

  static const List<String> cities = [
    'Bangalore',
    'Chennai',
    'New York',
    'Mumbai',
    'Delhi',
    'Tokyo',
    'Viana',
    'Porto',
    'Lisboa',
    'Braga',
    'Algarve',
    'Guimarães',
    'Esposende'
  ];

  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final TextEditingController _typeAheadController = TextEditingController();

  static List<String> getSuggestions(String query) => List.of(cities).where(
      (city) {
        return city.toLowerCase().contains(query.toLowerCase());
      }
  ).toList();

  Widget _buildCourseName() {

    return TypeAheadFormField(
      textFieldConfiguration: TextFieldConfiguration(
          controller: _typeAheadController,
          decoration: InputDecoration(
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10.0),
              ),
              filled: true,
              hintStyle: GoogleFonts.poppins(fontSize: 14, color: Colors.grey, fontWeight: FontWeight.w400),
              hintText: 'Insert week date (dd-mm-YYYY)',
              fillColor: Colors.white70
          ),
      ),

      suggestionsCallback: (pattern) {
        return getSuggestions(pattern);
      },

      itemBuilder: (context, String? suggestion) {
        return ListTile(
          title: Text(suggestion!),
        );
      },

      transitionBuilder: (context, suggestionsBox, controller) {
        return suggestionsBox;
      },

      onSuggestionSelected: (String? suggestion) {
        _typeAheadController.text = suggestion!;
      },

      validator: (String? value) {
        if (value!.isEmpty || !cities.contains(value)) {
          return 'Please select a course.';
        }
        return null;
      },

      onSaved: (value) => _courseName = value!,
    );
  }

  Widget _buildCourseYear() {

    return Row(
      mainAxisAlignment: MainAxisAlignment.start,
      children: [
        SizedBox(
          width: 200,
          child: TextFormField(
            keyboardType: TextInputType.number,
            decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10.0),
                ),
                filled: true,
                hintStyle: GoogleFonts.poppins(fontSize: 14, color: Colors.grey, fontWeight: FontWeight.w400),
                hintText: 'Select year...',
                fillColor: Colors.white70
            ),

            validator: (value) {
              if (value!.isEmpty) {
                return "Course year is required.";
              }

              int numberValue;
              try {
                numberValue = int.parse(value);
              } catch (e) {
                return 'Please insert a valid number.';
              }

              if (numberValue < 1 || numberValue >= 5) {
                return 'Value must be between 1 and 4.';
              }

              return null;
            },

            onSaved: (String? value) {
              _courseYear = value!;
            },
          ),
        ),
      ],
    );
  }

  Widget _buildWeekDate() {

    return TextFormField(
      decoration: InputDecoration(
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(10.0),
          ),
          filled: true,
          hintStyle: GoogleFonts.poppins(fontSize: 14, color: Colors.grey, fontWeight: FontWeight.w400),
          hintText: 'Insert week date (dd-mm-YYYY)',
          fillColor: Colors.white70
      ),

      validator: (value) {
        if (value!.isEmpty) {
          return "Week date is required.";
        }
        return null;
      },

      onSaved: (String? value) {
        _weekDate = value!;
      },

    );
  }

  Widget _buildCheckBoxes() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.start,
      children: <Widget> [

        Checkbox(
            value: _shiftFilter,
            onChanged: (bool? value) {
              setState(() {
                if (_jsonOnly == true && value! == true) {
                  _shiftFilter = value;
                }
                else if (_jsonOnly == false && value! == true) {
                  _shiftFilter = value;
                }
                else if (_jsonOnly == true && value! == false) {
                  _shiftFilter = value;
                }
                else {
                  _jsonOnly = true;
                  _shiftFilter = value!;
                }
              });
            },
            checkColor: Colors.white70,
            fillColor:  MaterialStateProperty.all<Color>(fadeBlue),
        ),

        Text("Filter Shifts" , style: GoogleFonts.poppins(fontSize: 22, color: text, fontWeight: FontWeight.w400)),
        const SizedBox(width: 12),

        Checkbox(
            value: _jsonOnly,
            onChanged: (bool? value) {
              setState(() {
                if (_shiftFilter == true && value! == true) {
                  _jsonOnly = value;
                }
                else if (_shiftFilter == false && value! == true) {
                  _jsonOnly = value;
                }
                else if (_shiftFilter == true && value! == false) {
                  _jsonOnly = value;
                }
                else {
                  _shiftFilter = true;
                  _jsonOnly = value!;
                }
              });
            },
            checkColor: Colors.white70,
            fillColor:  MaterialStateProperty.all<Color>(fadeBlue),
        ),

        Text("Json Only" , style: GoogleFonts.poppins(fontSize: 22, color: text, fontWeight: FontWeight.w400)),

      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget> [

          Container(
              alignment: Alignment.centerLeft,
              margin: const EdgeInsets.only(bottom: 15),
              child: Text("Select your course :" , style: GoogleFonts.poppins(fontSize: 24, color: text, fontWeight: FontWeight.w400))
          ),
          _buildCourseName(),
          const SizedBox(height: 14),

          Container(
              alignment: Alignment.centerLeft,
              margin: const EdgeInsets.only(bottom: 15),
              child: Text("Select a year :" , style: GoogleFonts.poppins(fontSize: 24, color: text, fontWeight: FontWeight.w400))
          ),
          _buildCourseYear(),
          const SizedBox(height: 14),

          Container(
              alignment: Alignment.centerLeft,
              margin: const EdgeInsets.only(bottom: 15),
              child: Text("Select week date :" , style: GoogleFonts.poppins(fontSize: 24, color: text, fontWeight: FontWeight.w400))
          ),
          _buildWeekDate(),
          const SizedBox(height: 24),

          _buildCheckBoxes(),
          Container(
              alignment: Alignment.centerLeft,
              margin: const EdgeInsets.only(bottom: 15, left: 6),
              child: Text("Select at least one of the checkboxes above." , style: GoogleFonts.poppins(fontSize: 12, color: text, fontWeight: FontWeight.w400))
          ),
          const SizedBox(height: 14),

          Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              ConstrainedBox(
                constraints: const BoxConstraints.tightFor(width: 150, height: 50),
                child: ElevatedButton(
                    onPressed: () {
                      if (!_formKey.currentState!.validate() || (_jsonOnly == false && _shiftFilter == false)) {
                        return;
                      }

                      _formKey.currentState!.save();
                      /* TODO: Processar os dados e isso. */
                      debugPrint(_courseYear);
                      debugPrint(_courseName);
                      debugPrint(_weekDate);
                      print(_jsonOnly);
                      print(_shiftFilter);
                    },
                    style: ButtonStyle(
                        backgroundColor: MaterialStateProperty.all<Color>(const Color.fromRGBO(74, 90, 232, 1)),
                        shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                            RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10.0),
                              side: BorderSide(color: fadeBlue),
                            )
                        )
                    ),
                    child: Text("Download" , style: GoogleFonts.poppins(fontSize: 20, color: Colors.white, fontWeight: FontWeight.w300)),
                ),
              ),
            ],
          )

        ],
      ),
    );
  }
}


