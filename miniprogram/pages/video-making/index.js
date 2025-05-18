// pages/video-making/index.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    tabIndex: 0, // 0: 真人素材, 1: 上传文案, 2: 上传图片
    videoPath: "",
    docText: "",
    imagePath: "",
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {},

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {},

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {},

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {},

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {},

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {},

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {},

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {},

  switchTab(e) {
    this.setData({ tabIndex: e.currentTarget.dataset.index });
  },

  uploadVideo() {
    wx.chooseVideo({
      maxDuration: 10,
      success: (res) => {
        this.setData({ videoPath: res.tempFilePath });
      },
    });
  },

  uploadDoc(e) {
    this.setData({ docText: e.detail.value });
  },

  uploadImage() {
    wx.chooseImage({
      count: 1,
      success: (res) => {
        this.setData({ imagePath: res.tempFilePaths[0] });
      },
    });
  },

  generateVideo() {
    wx.showToast({ title: "生成视频中...", icon: "loading" });
    // 这里可调用后端生成视频接口
    setTimeout(() => {
      wx.showToast({ title: "生成成功", icon: "success" });
    }, 1500);
  },
});
