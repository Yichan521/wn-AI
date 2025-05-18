// pages/writting/index.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    tabIndex: 0, // 0: 产品介绍文案, 1: 社交媒体带货文案
    productName: "",
    productOrigin: "",
    productFeature: "",
    productDesc: "",
    productImage: "",
    productSellingPoint: "",
    result: "",
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

  onInput(e) {
    const { field } = e.currentTarget.dataset;
    this.setData({ [field]: e.detail.value });
  },

  chooseImage() {
    wx.chooseImage({
      count: 1,
      success: (res) => {
        this.setData({ productImage: res.tempFilePaths[0] });
      },
    });
  },

  generateCopy() {
    const {
      tabIndex,
      productName,
      productOrigin,
      productFeature,
      productDesc,
      productSellingPoint,
    } = this.data;
    wx.showLoading({ title: "别急..." });

    // 判断tab，选择不同接口和参数
    let url = "";
    let data = {};
    if (tabIndex === 0) {
      // 产品介绍文案
      url = "http://127.0.0.1:5000/api/gen_copy";
      data = { productName, productOrigin, productFeature, productDesc };
    } else if (tabIndex === 1) {
      // 社交媒体带货
      url = "http://127.0.0.1:5000/api/gen_social_copy";
      data = { productName, productOrigin, productSellingPoint };
    }
    wx.request({
      url,
      method: "POST",
      data,
      header: {
        "content-type": "application/json",
      },
      success: (res) => {
        wx.hideLoading();
        if (res.data && res.data.result) {
          this.setData({ result: res.data.result });
        } else {
          this.setData({ result: "生成失败，请稍后重试" });
        }
      },
      fail: () => {
        wx.hideLoading();
        this.setData({ result: "网络错误，请稍后重试" });
      },
    });
  },

  toVideo() {
    wx.showToast({ title: "跳转为视频功能", icon: "none" });
  },
});
