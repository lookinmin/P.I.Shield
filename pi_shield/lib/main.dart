import 'dart:async';
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
//import 'package:path/path.dart' show join;
//import 'package:path_provider/path_provider.dart';
import 'package:image_picker/image_picker.dart';
import 'package:image_gallery_saver/image_gallery_saver.dart';
import 'dart:typed_data';
// import 'package:cached_network_image/cached_network_image.dart';
// import 'package:dio/dio.dart';
import 'package:intl/intl.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CameraDemo',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: UseCamera(),
    );
  }
}

class UseCamera extends StatefulWidget {
  @override
  _UseCameraState createState() => _UseCameraState();
}

class _UseCameraState extends State<UseCamera> {
  File? _image;
  final picker = ImagePicker();

  late ByteData imgData;

  _save(BuildContext context, File? image) async {
    var now = DateTime.now();
    String formatDate = DateFormat('yyyyMMdd_HHmmss').format(now);
    final bytes = await image!.readAsBytes();
    final result = await ImageGallerySaver.saveImage(
      bytes,
      quality: 60,
      name: "PI Shield_$formatDate", //사전 저장하는 이름
    );

    Navigator.pop(context);
    print(result);
  }

  @override
  Widget build(BuildContext context) {
    Future getImage(ImageSource imageSource) async {
      final pickedFile = await picker.getImage(source: imageSource);

      setState(() {
        _image = File(pickedFile!.path);
      });
    }

    return Scaffold(
      body: SafeArea(
          child: Column(
        children: [
          ElevatedButton(
              onPressed: () {
                getImage(ImageSource.camera);
              },
              child: Text('Camera')),
          ElevatedButton(
              onPressed: () {
                getImage(ImageSource.gallery);
              },
              child: Text('Gallery')),
          ElevatedButton(
            onPressed: () {
              showDialog<String>(
                  context: context,
                  builder: (BuildContext context) => AlertDialog(
                        title: Text("저장하시겠습니까?"),
                        actions: [
                          OutlinedButton(
                              onPressed: () {
                                _save(context, _image);
                              },
                              child: Text("저장")),
                          OutlinedButton(
                              onPressed: () => Navigator.pop(context, 'Cancel'),
                              child: Text("취소")),
                        ],
                      ));
            },
            child: Text('저장'),
          ),
          showImage(),
        ],
      )),
    );
  }

  Widget showImage() {
    if (_image == null) {
      return Container();
    } else {
      return Image.file(_image!);
    }
  }
}
