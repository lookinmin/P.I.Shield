import 'dart:async';
import 'dart:ffi';
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
import 'splash_screen.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CameraDemo',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.blue),
      initialRoute: '/',
      routes: {"/": (context) => Splash()},
      //home: UseCamera(),
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
  int ratioMode = 0;

  _save(BuildContext context, File? image) async {
    var now = DateTime.now();
    String formatDate = DateFormat('yyyyMMdd_HHmmss').format(now);
    Uint8List bytes = await image!.readAsBytes();
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
    var size = MediaQuery.of(context).size;
    //이미지 경로 받아오기
    Future getImage(ImageSource imageSource) async {
      final pickedFile = await picker.getImage(source: imageSource);

      setState(() {
        _image = File(pickedFile!.path);
      });
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Ping-pong',
          style:
              TextStyle(color: Color.fromARGB(255, 6, 29, 149), fontSize: 15),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0.0,
      ),
      body: SafeArea(
          child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          //우측 상단 블러 저장
          Container(
              alignment: Alignment.bottomRight,
              padding: const EdgeInsets.only(right: 10),
              child: _image != null
                  ? IconButton(
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
                                        onPressed: () =>
                                            Navigator.pop(context, 'Cancel'),
                                        child: Text("취소")),
                                  ],
                                ));
                      },
                      icon: const Icon(
                        Icons.bookmark_add_outlined,
                        color: Color.fromARGB(255, 6, 29, 149),
                      ),
                      iconSize: 35,
                    )
                  : const SizedBox()),

          //상단 비율 박스
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _image != null
                  ? Row(
                      children: [
                        TextButton(
                            onPressed: () => setState(() {
                                  ratioMode = 1;
                                }),
                            child: const Text(
                              '16:9',
                              style: TextStyle(fontSize: 15),
                            )),
                        TextButton(
                            onPressed: () => setState(() {
                                  ratioMode = 2;
                                }),
                            child: const Text(
                              '4:3',
                              style: TextStyle(fontSize: 15),
                            )),
                        TextButton(
                            onPressed: () => setState(() {
                                  ratioMode = 3;
                                }),
                            child: const Text(
                              '1:1',
                              style: TextStyle(fontSize: 15),
                            ))
                      ],
                    )
                  : const SizedBox()
            ],
          ),
          showImage(size),

          //하단 카메라 및 갤러리 박스
          Container(
            padding: const EdgeInsets.only(top: 20),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                IconButton(
                  onPressed: () {
                    getImage(ImageSource.camera);
                  },
                  icon: const Icon(
                    Icons.photo_camera_outlined,
                    color: Color.fromARGB(255, 6, 29, 149),
                  ),
                  iconSize: 40,
                ),
                IconButton(
                    onPressed: () {
                      getImage(ImageSource.gallery);
                    },
                    icon: const Icon(Icons.photo_library_outlined,
                        color: Color.fromARGB(255, 6, 29, 149)),
                    iconSize: 35),
              ],
            ),
          ),
          const SizedBox(
            height: 40,
          )
        ],
      )),
    );
  }

  //사진 들어올 박스
  Widget showImage(size) {
    if (_image == null) {
      return Container(
        color: const Color.fromARGB(255, 232, 232, 232),
        width: size.width,
        height: size.height * 0.5,
        child: Image.asset('images/logo.png'),
      );
    } else {
      return Container(
          color: const Color.fromARGB(255, 232, 232, 232),
          width: size.width,
          height: ratioMode == 0
              ? size * 0.5
              : (ratioMode == 1
                  ? size.width * 16 / 9
                  : (ratioMode == 2 ? size.width * 4 / 3 : size.width)),
          // height: ratioMode == 0 ? size.height * 0.5 : size.width * 9 / 16,
          // height: size.height * 0.5,
          child: Image.file(_image!));
    }
  }
}
