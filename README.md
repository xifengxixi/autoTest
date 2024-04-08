# AutoTest

#### 一、介绍

本框架为企业实际落地的自动化测试框架，包含**接口自动化**和**UI自动化**。

- 项目参与者：溪风习习
- 个人语雀地址：https://www.yuque.com/xifengxixi
- 技术支持邮箱：1107872406@qq.com

如果对您有帮助，请点亮本项目的小星星，不胜感激。

#### 二、项目结构

项目结构说明

```python
autoTest
│  README.en.md
│  README.md
│  
├─api_frame                                 # 接口自动化框架
│  │  config.py                             # 接口框架配置文件
│  │  conftest.py                           # 钩子函数文件
│  │  pytest.ini                            # pytest配置文件
│  │  requirements.txt                      # 依赖文件
│  │  run.py                                # 运行接口用例入口
│  │
│  ├─apiObject                              # 接口api文件
│  │
│  ├─logs                                   # 接口日志
│  │
│  ├─reports                                # 接口报告
│  │
│  ├─testCase                               # 接口用例
│  │
│  ├─testData                               # 接口数据
│  │
│  └─utils                                  # 接口工具
│
└─ui_frame
    │  config.py                            # UI框架配置文件
    │  conftest.py                          # 钩子函数文件
    │  run.py                               # 运行UI用例入口
    │  runpytest_jenkins.py					
    │  runpytest_uicases_jenkins.py
    │  runpytest_uitask_jenkins.py
    │  ui_session.json                      # UI浏览器session文件
    │
    ├─logs                                  # UI日志
    │
    ├─pageObject                            # UI页面对象（PO模式）
    │
    ├─reports                               # UI报告
    │
    ├─testCase                              # UI用例
    │
    ├─testData                              # UI数据
    │
    └─utils                                 # UI工具
```

#### 三、使用说明

##### 3.1 接口框架

###### 3.1.1 接口用例编写

1. 在 api_frmae\apiObject 文件夹下编写接口api文件
   - 推荐按模块进行分类
   - base，存放一些公共方法，如登录、加解密、及用例可使用的公共方法等，可自由扩展
   - module，存放各模块的接口api
2. 在 api_frame\testCase 文件夹下编写接口用例文件
   - 推荐按模块进行分类
   - module，存放各模块的接口用例
   - 用例文件setup_class，存放用例类前置公共方法，如获取token等
   - 用例文件setup_method，存放时间戳等
   - 用例文件teardown_method，可进行数据清理
   - 用例文件teardown_class，一般进行数据清理等
3. 运行用例
   - 运行单个用例，直接在pycharm对应用例运行即可
   - 运行多个用例并生成报告，入口在run.py文件

> 接口api及用例文件，本项目均有例子，可供参考

###### 3.1.2 其它说明

1. 配置文件放在config.py中，包含环境url、超时时间、日志等
2. 钩子函数放在conftest.py中，包含安装缺失库、报告处理等钩子
3. pytest配置放在pytest.ini中，包含标签等
4. run.py为用例运行文件，可配置参数运行用例并生成报告
5. 工具类放在utils下，包含数据库处理工具、日志工具、加密工具、接口请求工具等
6. 用例运行前需要将api_frame、api_frame\testCase标记为Sources Root文件夹

##### 3.2 UI框架

###### 3.2.1 UI用例编写

1. 在 ui_frame\pageObject 文件夹下编写UI页面对象文件

   - 推荐按模块进行分类

   - common，存放组件、基础方法
   - module，存放各模块的用例对象文件。同一模块各页面通用方法，推荐放basePage，其余功能按页面放对应业务Page

2. 在 ui_frame\testCase 文件夹下编写UI用例文件

   - 推荐按模块进行分类
   - 模块的通用前置方法，如创建数据等，可放在模块的conftest.py文件
   - 使用allure.epic\allure.feature\allure.story等对用例进行标记，可在allure报告查看
   - 用例文件setup_class，存放页面、接口类对象、driver等
   - 用例文件setup_method，存放时间戳等
   - 用例文件teardown_method，保留浏览器一个页签等
   - 用例文件teardown_class，进行数据清理等

3. 运行用例

   - 运行单个用例，直接在pycharm对应用例运行即可
   - 运行多个用例并生成报告，入口在run.py文件
   - 可根据需要定制jenkins等运行用例入口

> UI页面对象及用例文件，本项目均有例子，可供参考

###### 3.2.3 其它说明

1. 配置文件在config.py中，包含selenium和路径相关配置等
2. 钩子函数在fonftest.py中，包含失败截图、启动浏览器、类登录等钩子
3. ui_session.json，存放当前浏览器session信息
4. pageObject\common\components，存放各种前端组件方法，包括按钮(button)、复选框(checkbox)、日期选择器(datePickerUi)、时间选择器(TimePickerUi)、菜单(menu)、上传(upload)等各类组件。可自由扩展
5. pageObject\common\base.py，存放所有基础方法，包括定位元素、打开url、输入、悬浮、拖拽、滚动、js操作、切换frame、切换window等。可自由扩展
6. reports，包括报告文件夹、截图文件夹、缓存文件夹等
7. utils，包括allure报告分析工具、日志工具等
8. 框架支持多浏览器多截图，适合不同角色的场景
9. config.py若打开调试模式，debug=True，则运行用例的时候首先在当前打开的浏览器（自动化打开的浏览器）中接着运行用例
10. 用例setup_class，不能直接调用conftest中的class_login，因此需要以fixtrue的方式进行登录，具体方式查看项目中的例子
11. UI框架可调用接口框架的接口，在用例编写时可结合接口和UI，提升用例运行效率，同时可避免对同一功能进行多次UI验证
12. 用例运行前需要将ui_frame、ui_frame\pageObject标记为Sources Root文件夹

#### 四、报告效果

##### 4.1 接口报告

![apiReport1.png](.\api_frame\testData\images\apiReport1.png)

##### 4.2 UI报告

![uiReport1.png](.\ui_frame\testData\images\uiReport1.png)

![uiReport2.png](.\ui_frame\testData\images\uiReport2.png)

![uiReport3.png](.\ui_frame\testData\images\uiReport3.png)

![uiReport4.png](.\ui_frame\testData\images\uiReport4.png)