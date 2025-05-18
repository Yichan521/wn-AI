Page({
  data: {
    goodsList: [
      {
        _id: "1",
        title: "商品1",
        price: 1,
      },
    ],
    showTip: false,
    title: "",
    content: "",
  },

  onLoad() {
    // this.fetchGoodsList();
  },

  async fetchGoodsList() {
    this.setData({ isLoading: true });
    try {
      const res = await wx.cloud.callFunction({
        name: "quickstartFunctions",
        data: { type: "fetchGoodsList" },
      });
      const goodsList = res?.result?.dataList || [];
      this.setData({
        isLoading: false,
        goodsList,
      });
    } catch (e) {
      const { errCode, errMsg } = e;
      if (errMsg.includes("Environment not found")) {
        this.setData({
          showTip: true,
          title: "云开发环境未找到",
          content:
            "如果已经开通云开发，请检查环境ID与 `miniprogram/app.js` 中的 `env` 参数是否一致。",
        });
        return;
      }
      if (errMsg.includes("FunctionName parameter could not be found")) {
        this.setData({
          showTip: true,
          title: "请上传云函数",
          content:
            "按照教程指引更新云函数，保存完成后，在'cloudfunctions/quickstartFunctions'目录右键，选择【上传并部署-云端安装依赖】，等待云函数上传完成后重试。",
        });
        return;
      }
    }
  },

  async generateMPCode() {
    wx.showLoading();
    try {
      const resp = await wx.cloud.callFunction({
        name: "quickstartFunctions",
        data: {
          type: "genMpQrcode",
          pagePath: "pages/goods-list/index",
        },
      });
      this.setData({ codeModalVisible: true, codeImageSrc: resp?.result });
      wx.hideLoading();
    } catch (e) {
      wx.hideLoading();
      const { errCode, errMsg } = e;
      if (errMsg.includes("Environment not found")) {
        this.setData({
          showTip: true,
          title: "云开发环境未找到",
          content:
            "如果已经开通云开发，请检查环境ID与 `miniprogram/app.js` 中的 `env` 参数是否一致。",
        });
        return;
      }
      if (errMsg.includes("FunctionName parameter could not be found")) {
        this.setData({
          showTip: true,
          title: "请上传云函数",
          content:
            "按照教程指引更新云函数，保存完成后，在'cloudfunctions/quickstartFunctions'目录右键，选择【上传并部署-云端安装依赖】，等待云函数上传完成后重试。",
        });
        return;
      }
    }
  },
});
