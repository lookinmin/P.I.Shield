import 'dart:async';
import 'dart:ffi';
import 'dart:io';
import 'package:flutter/material.dart';
//import 'package:path/path.dart' show join;
//import 'package:path_provider/path_provider.dart';
import 'package:image_picker/image_picker.dart';
import 'package:image_gallery_saver/image_gallery_saver.dart';
// import 'package:cached_network_image/cached_network_image.dart';
// import 'package:dio/dio.dart';
import 'package:intl/intl.dart';
import 'splash_screen.dart';
import 'package:image/image.dart' as IMG;

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

  //찍은 사진을 갤러리에 저장
  _save(BuildContext context, File? image) async {
    var now = DateTime.now();
    String formatDate = DateFormat('yyyyMMdd_HHmmss').format(now);
    List<int> bytes = await image!.readAsBytes();
    final originImg = IMG.decodeImage(bytes);
    IMG.Image fixedImg;
    fixedImg = IMG.copyRotate(originImg!, 0);
    final fixedFile = await image.writeAsBytes(IMG.encodeJpg(fixedImg));
    await ImageGallerySaver.saveFile(
      fixedFile.path,
      name: "PI Shield_$formatDate", //사전 저장하는 이름
    );
    Navigator.pop(context);
  }

  // _cropImage(mode, File image) async {
  //   if (mode == 1) {
  //     print('asdfasdf');
  //     setState(() {
  //       copyImage1 =
  //           ResizeImage(Image.file(image).image, height: 100, width: 100);
  //     });
  //   }
  // }

  @override
  Widget build(BuildContext context) {
    var size = MediaQuery.of(context).size;
    //이미지 경로 받아오기
    Future getImage(ImageSource imageSource) async {
      final pickedFile =
          await picker.getImage(source: imageSource, imageQuality: 60);

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
            padding: const EdgeInsets.symmetric(horizontal: 10),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                //api 호출 버튼
                InkWell(
                  onTap: () {},
                  child: Column(
                    children: [
                      Image.asset(
                        'images/api.png',
                        fit: BoxFit.fill,
                        width: 40,
                        height: 40,
                      ),
                      const SizedBox(
                        height: 5,
                      ),
                      const Text(
                        'Blur',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(
                        height: 10,
                      ),
                    ],
                  ),
                ),
                Column(
                  children: [
                    InkWell(
                      onTap: () {
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
                      child: Column(
                        children: [
                          Image.asset(
                            'images/save.png',
                            fit: BoxFit.fill,
                            width: 40,
                            height: 40,
                          ),
                          const SizedBox(
                            height: 5,
                          ),
                          const Text(
                            'Save',
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(
                            height: 10,
                          ),
                        ],
                      ),
                    ),
                  ],
                )
              ],
            ),
          ),

          showImage(size),

          //하단 카메라 및 갤러리 박스
          Container(
            padding: const EdgeInsets.only(top: 20),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Column(
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
                    const Text('Camera',
                        style: TextStyle(fontWeight: FontWeight.bold))
                  ],
                ),
                Column(
                  children: [
                    IconButton(
                        onPressed: () {
                          getImage(ImageSource.gallery);
                        },
                        icon: const Icon(Icons.photo_library_outlined,
                            color: Color.fromARGB(255, 6, 29, 149)),
                        iconSize: 35),
                    const Text(
                      'Gallery',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    )
                  ],
                ),
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
      return Center(child: Image.file(_image!));
    }
  }
}
