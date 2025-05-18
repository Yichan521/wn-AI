// pages/poster-making/index.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    productName: "",
    posterTitle: "",
    content: "",
    style: "",
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

  onInput(e) {
    const { field } = e.currentTarget.dataset;
    this.setData({ [field]: e.detail.value });
  },

  generatePoster() {
    wx.showToast({ title: "生成海报中...", icon: "loading" });
    // 这里可调用后端生成海报接口
    setTimeout(() => {
      this.setData({ result: "这是AI生成的海报内容示例。" });
      wx.showToast({ title: "生成成功", icon: "success" });
    }, 1500);
  },

  downloadPoster() {
    wx.showToast({ title: "下载海报", icon: "none" });
    // 这里可实现下载逻辑
  },
});
