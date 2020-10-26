<template>
  <v-container class="fill-height">
    <v-row>
      <v-col cols="auto mx-auto">
        <v-card id="camera" class="mx-auto rounded" max-width="560">
          <v-card-title primary-title class="justify-center">人脸识别</v-card-title>
          <video
            autoplay
            ref="video"
            id="video"
            width="560"
            height="420"
            muted
            @loadedmetadata="startDetect"
          ></video>
          <canvas id="overlay" ref="overlay" width="0" height="0"></canvas>

          <v-card-actions class="mt-5">
            <v-switch v-model="switchColloect" color="green" class="ml-5" inset label="人脸采集"></v-switch>
            <v-spacer></v-spacer>
            <v-btn x-large outlined color="success" @click="startCapture">开始</v-btn>
            <v-btn x-large outlined color="red" @click="stopCapture">关闭</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <!-- <v-divider vertical></v-divider>
      <v-col>
        <check-record></check-record>
      </v-col>-->
    </v-row>
    <v-snackbar v-model="snackbar" rounded="pill" :timeout="timeout">
      {{ text }}
      <template v-slot:action="{ attrs }">
        <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">关闭</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import FaceCheckRecord from "@/components/FaceCheckRecord";
import * as faceapi from "face-api.js";
import { mapState } from "vuex";
export default {
  name: "faceRecord",
  components: {
    "check-record": FaceCheckRecord
  },
  data() {
    return {
      snackbar: false,
      text: "请对准摄像头，不要乱动，等待模型加载完毕！",
      timeout: 3000,
      switchColloect: false,
      stream: "",
      net: "tinyFaceDetector",
      detectFace: "detectSingleFace",
      options: null,
      timeInterval: null,
      disabled: false,
      face_data: [],
      flag: false,
      message: "",
      record_id: null
    };
  },
  computed: {
    ...mapState({ employee_id: "userid" }),
    sendAmount() {
      if (this.switchColloect) {
        return 5;
      } else {
        return 3;
      }
    }
  },
  mounted() {
    // this.changeEmployee("E000004", 1);
    // console.log(typeof JSON.stringify({ code: 0 }));
    this.initModel();
    this.axios
      .get(this.SERVICE_PATH + "record_id", {
        params: {
          employee_id: this.employee_id
        }
      })
      .then(res => {
        let record_id = res.data.record_id;
        this.record_id = record_id;
        this.$store.commit("getRecord", record_id);
        // console.log(this.$store.state.record_id)
      });
  },
  methods: {
    // ...mapMutations(["changeEmployee"]),
    /**
     * 开始检测人脸
     */
    startDetect() {
      let amount = this.sendAmount;
      this.face_data = [];
      this.flag = false;
      const canvas = this.$refs.overlay;
      const dims = faceapi.matchDimensions(canvas, {
        width: this.$refs.video.width,
        height: this.$refs.video.height
      });
      console.log("开始检测");
      this.timeInterval = setInterval(() => {
        this.getFace(canvas, dims, amount);
      }, 100);
    },

    /**
     * 获取人脸
     */
    async getFace(canvas, dims, amount) {
      const detection = await faceapi[this.detectFace](
        //检测人脸
        this.$refs.video,
        this.options
      )
        .withFaceLandmarks()
        .withFaceDescriptor();
      const detections = [];

      if (detection != undefined) {
        detections.push(detection); //获取图片需要用到detection的数组
        const resizedDetection = faceapi.resizeResults(detection, dims);
        canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
        // faceapi.draw.drawDetections(canvas, resizedDetection); //画出检测框
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetection); //画出68个特征点
        if (this.face_data.length < amount) {
          // console.log(Array.from(detection.descriptor));
          // console.log(typeof Array.from(detection.descriptor));
          // console.log([1,2])
          // console.log(typeof [1, 2]);
          // console.log(detection.descriptor);
          const faceImages = await faceapi.extractFaces(
            //提取框内的脸
            this.$refs.video,
            detections.map(res => res.detection)
          );

          faceImages.forEach(
            canvas => {
              let base64Img = canvas.toDataURL("image/png");
              this.face_data.push(base64Img);
            }
            // this.$refs.canvasBox.appendChild(canvas)
          );
        } else {
          if (this.flag == false) {
            console.log("sent");
            if (amount == 3) {
              this.sendFaceVerifyData();
            } else {
              this.sendFaceCollectData();
            }

            this.flag = true;
          }

          // clearInterval(this.timeInterval);
        }
      } else {
        canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
      }
    },
    /**
     * 打开摄像头
     */
    startCapture() {
      this.text = "请对准摄像头，不要乱动，等待模型加载完毕！"
      this.snackbar = true;
      console.log("打开");
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(
          stream => {
            console.log(stream);
            this.stream = stream;
            this.$refs.video.srcObject = this.stream;
            this.$refs.video.play();
          },
          err => console.log(err)
        );
      }
    },
    /**
     * 关闭摄像头，清空画布
     */
    stopCapture() {
      if (this.timeInterval != null) {
        clearInterval(this.timeInterval);
      }
      this.$refs.video.pause();
      if (typeof this.stream === "object") {
        this.stream.getTracks().forEach(track => track.stop());

        this.stream = "";
        this.$refs.video.srcObject = null;
      }

      setTimeout(() => {
        if (this.$refs.overlay != undefined) {
          this.$refs.overlay
            .getContext("2d")
            .clearRect(
              0,
              0,
              this.$refs.overlay.width,
              this.$refs.overlay.height
            );
        }
      }, 100);
      console.log("关闭");
    },
    /**
     * 加载人脸检测模型
     */
    async initModel() {
      await faceapi.nets[this.net].loadFromUri("./models");
      await faceapi.loadFaceLandmarkModel("./models");
      await faceapi.loadFaceRecognitionModel("./models");
      // 根据模型参数识别调整结果
      switch (this.net) {
        case "ssdMobilenetv1":
          this.options = new faceapi.SsdMobilenetv1Options({
            minConfidence: 0.5, // 0.1 ~ 0.9
            inputSize: 224
          });
          break;
        case "tinyFaceDetector":
          this.options = new faceapi.TinyFaceDetectorOptions({
            // inputSize: 512, // 160 224 320 416 512 608
            inputSize: 224,
            scoreThreshold: 0.5 // 0.1 ~ 0.9
          });
          break;
        case "mtcnn":
          this.options = new faceapi.MtcnnOptions({
            minFaceSize: 20, // 0.1 ~ 0.9
            scaleFactor: 0.709 // 0.1 ~ 0.9
          });
          break;
        default:
          break;
      }
      console.log("模型加载完毕！");
    },
    /**
     * 向服务器发送检测到的人脸
     */
    sendFaceVerifyData() {
      let data = { face_data: this.face_data };
      // console.log(JSON.stringify(data));
      this.axios
        .post(this.SERVICE_PATH + "face/verify", JSON.stringify(data), {
          params: {
            employee_id: this.employee_id,
            setting_id: 1,
          },
          headers: {
            "Content-Type": "application/json"
          }
        })
        .then(res => {
          if (res.data.code === 0) {
            let record_id = res.data.record_id;
            this.$store.commit("getRecord", this.record_id);
            console.log(this.$store.state.record_id);
            this.message = `您于${res.data.nowtime}打卡成功！`;
          } else {
            this.message = "识别失败， 请重试！";
          }
          this.snackbar = true;
          this.text = this.message;
        });
    },
    sendFaceCollectData() {
      let data = { face_data: this.face_data };
      // console.log(JSON.stringify(data));
      this.axios
        .post(this.SERVICE_PATH + "face/save", JSON.stringify(data), {
          params: {
            employee_id: this.employee_id,
            record_id: this.$store.state.record_id
          },
          headers: {
            "Content-Type": "application/json"
          }
        })
        .then(res => {
          this.record_id = res.data.record_id;
          console.log(res);
          this.$store.commit("getRecord", this.record_id);
          console.log(this.$store.state.record_id);
          if (res.data.code === 0) {
            this.message = "收集数据成功！";
          } else {
            this.message = "收集失败， 请重试！";
          }
          this.snackbar = true;
          this.text = this.message;
        });
    }
  },
  beforeDestroy() {
    this.stopCapture();
  }
};
</script>


<style scoped>
#video {
  background-color: #000000;
  position: relative;
  border-radius: 5%;
  /* border-radius: 50%;
  object-fit: cover;  */
  -webkit-transform: scaleX(-1);
  transform: scaleX(-1);
}
#overlay {
  position: absolute;
  margin-left: -560px;
  -webkit-transform: scaleX(-1);
  transform: scaleX(-1);
}
/* border-radius: 50%;
  object-fit: cover;  */
</style>