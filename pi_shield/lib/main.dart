import 'dart:async';
import 'dart:ffi';
import 'dart:io';
import 'package:cached_network_image/cached_network_image.dart';
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
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:dio/dio.dart';

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

  bool flag = true;

  String blurUrl = "";

  //찍은 사진을 갤러리에 저장
  _save(BuildContext context, File? image) async {
    setState(() {
      flag = !flag;
    });
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

  void _callAPI() async {
    print("CALL API");

    List<int> bytes = await _image!.readAsBytes();
    final originImg = IMG.decodeImage(bytes);
    IMG.Image fixedImg;
    fixedImg = IMG.copyRotate(originImg!, 0);
    final fixedFile = await _image!.writeAsBytes(IMG.encodeJpg(fixedImg));

    setState(() {
      _image = fixedFile;
    });

    var dio = Dio();
    var formData = FormData.fromMap({
      'file':
          await MultipartFile.fromFile(fixedFile.path, filename: fixedFile.path)
    });
    var response = await dio
        .post('https://late-jokes-try-175-205-84-241.loca.lt/uploadfile/',
            data: formData)
        .then((value) {
      var result = dio.download(
          'https://late-jokes-try-175-205-84-241.loca.lt/downloadfile/${value.data['fileurl']}',
          _image!.path);

      setState(() {
        blurUrl =
            'https://late-jokes-try-175-205-84-241.loca.lt/downloadfile/${value.data['fileurl']}';
        flag = false;
      });
    });
  }

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
        title: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: const [
            Text(
              'Ping-pong',
              style: TextStyle(
                  color: Color.fromARGB(255, 6, 29, 149), fontSize: 15),
            ),
            Text(
              'P.I.\n Shield',
              textAlign: TextAlign.end,
              style: TextStyle(
                  color: Color.fromARGB(255, 6, 29, 149), fontSize: 15),
            )
          ],
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
            padding: const EdgeInsets.fromLTRB(10, 0, 10, 20),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                //api 호출 버튼
                InkWell(
                  onTap: () {
                    //api 호출

                    _callAPI();
                  },
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
                                          setState(() {
                                            flag = true;
                                          });
                                          _save(context, _image);
                                        },
                                        child: Text("저장")),
                                    OutlinedButton(
                                        onPressed: () {
                                          setState(() {
                                            flag = true;
                                          });
                                          Navigator.pop(context, 'Cancel');
                                        },
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
          Camera_Gallery(getImage),
          const SizedBox(
            height: 40,
          ),

          // const Text('당신의 소중한 개인정보')
        ],
      )),
      bottomNavigationBar: BottomAppBar(
        color: Colors.transparent,
        elevation: 0.0,
        child: Container(
            padding: EdgeInsets.fromLTRB(0, 0, 0, 15),
            child: const Text(
              '©Copyright 2022. 핑퐁(Ping-pong)',
              textAlign: TextAlign.center,
              style: TextStyle(
                  color: Color.fromARGB(255, 174, 174, 174), fontSize: 15),
            )),
      ),
    );
  }

  Container Camera_Gallery(Future<dynamic> getImage(ImageSource imageSource)) {
    return Container(
      padding: const EdgeInsets.only(top: 30),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Column(
            children: [
              IconButton(
                onPressed: () {
                  setState(() {
                    getImage(ImageSource.camera);
                    flag = true;
                  });
                  // _callAPI();
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
                    setState(() {
                      flag = true;
                    });
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
      return Center(
          child: flag
              ? Image.file(File(_image!.path))
              : CachedNetworkImage(
                  imageUrl: blurUrl,
                ));
      //Image.file(File(_image!.path)
    }
  }
}
