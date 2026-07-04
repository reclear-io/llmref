# https://jasminides.com/ llms-full.txt

## Programming Solutions Blog
Welcome to my blog

前言 前段时间看到了一个项目 mi-gpt ,可以将你的小爱音箱接入 gpt，改造成专属于你的语音助手。
接下来就由作者来介绍小爱同学从零接入 deepseek 的过程。
设置环境变量和配置文件 mi-gpt 有两种部署方式，一是使用 docker 部署，二是使用 Node.js 进行部署，本文使用 docker 进行部署使用。
需要提供两个文件 .env 和 .migpt.js 文件，.migpt.js 是配置文件，包括一些配置，.env 是环境变量文件，存放 gpt 密钥相关文件。文件的例子可以从仓库里复制，然后进行相应的修改。
启动 使用以下命令启动 docker:
docker run -d --env-file $(pwd)/.env -v $(pwd)/.migpt.js:/app/.migpt.js idootop/mi-gpt:latest windows 环境下需要将$(pwd) 替换为绝对路径。
启动后可以通过 callAIKeywords 设置的关键字调用 ai 来响应用户的消息。
小结 本文介绍了使用 mi-gpt 升级你的闲置的小爱音箱，通过简单的测试和使用，个人感觉还不够完善，稳定性不够好，感兴趣的读者可以根据本文的内容进行自行搭建尝试。
参考 https://github.com/idootop/mi-gpt

 [post link to 使用 gpt 改造你的小米音箱](https://jasminides.com/posts/mi_gpt/)

前言 今天在编译构建一个 node.js 项目时，在构建过程中遇到了一些问题，本文将记录问题及对应的解决方案。
问题 1 在执行 npm run build 遇到此提示：
error Expected linebreaks to be 'LF' but found 'CRLF' linebreak-style 根据信息可以看出是 eslint 的报错，查看 .eslintrc.js 文件，修改 linebreak-style 对应的行：
'linebreak-style': \['error', process.platform === 'win32' ? 'windows' : 'unix'\], 重新运行命令，顺利构建成功。
这个问题的原因是项目的作者可能是使用 Linux 或 Mac 构建的，没有考虑 Windows 的情况，通过这行配置，可以根据运行的环境来决定 lint 规则。
问题 2 在执行 npm start 遇到了第二个问题：
Generating browser application bundles (phase: building)...node:internal/crypto/hash:79 this\[kHandle\] = new \_Hash(algorithm, xofLen, algorithmId, getHashCache()); ^ Error: error:0308010C:digital envelope routines::unsupported at new Hash (node:internal/crypto/hash:79:19) at Object.createHash (node:crypto:139:10) at BulkUpdateDecorator.hashFactory (D:\\code\\xx\\node\_modules\\webpack\\lib\\util\\createHash.js:145:18) at BulkUpdateDecorator.update (D:\\code\\xx\\node\_modules\\webpack\\lib\\util\\createHash.js:46:50) at RawSource.updateHash (D:\\code\\xx\\node\_modules\\webpack\\node\_modules\\webpack-sources\\lib\\RawSource.js:77:8) at NormalModule.\_initBuildHash (D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:880:17) at handleParseResult (D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:946:10) at D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:1040:4 at processResult (D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:755:11) at D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:819:5 { opensslErrorStack: \[ 'error:03000086:digital envelope routines::initialization error', 'error:0308010C:digital envelope routines::unsupported' \], library: 'digital envelope routines', reason: 'unsupported', code: 'ERR\_OSSL\_EVP\_UNSUPPORTED' } 根据这个报错，推测可能是啥 hash 算法不支持，通过查阅相关资料，得到以下解决方案：
...

 [post link to node.js 项目构建问题及解决](https://jasminides.com/posts/node_build_error/)

问题 最近在使用 go 解析 csv 文件时，读取并打印 csv 的每行内容时，读取到第 11 行时，程序报错，提示：
record on line 11: wrong number of fields 分析 遇到这个问题，我第一反应是 csv 文件的格式有问题，于是我使用 cat 命令查看 csv 文件，发现 csv 文件的格式是正确的，没有问题。 并查看分隔符是正确的，于是可以得出 csv 文件是没有问题的。
接下来就查看所使用的标准库 encoding/csv，通过查阅文档及 issue, 发现 csv 包中的 FieldsPerRecord 字段，FieldsPerRecord 表示 csv 文件每行的预期字段数， 如果为正数，则读取的每条记录都必须有对应的字段数，如果为 0，则会以第一条记录的数量为标准，接下来每行都必须有对应的字段数，如果为负数，则不会检查字段数。
修改后的代码如下：
package main import ( "encoding/csv" "fmt" "io" "log" "os" ) func main() { file, err := os.Open("./xx.csv") if err != nil { log.Fatal(err) } defer file.Close() // 创建一个 CSV reader reader := csv.NewReader(file) reader.FieldsPerRecord = -1 // 循环读取 CSV 文件中的每一行数据 for { record, err := reader.Read() if err == io.EOF { break } if err != nil { log.Fatal(err) } // 处理每一行数据 fmt.Println(record) fmt.Println(len(record)) } } 小结 本文记录了在使用 go 解析 csv 时遇到字段数不匹配的问题，并分析了问题的原因，并给出了相应的解决方法。
...

 [post link to go 解析 csv 文件报错](https://jasminides.com/posts/read_csv_error/)

前言 电子邮件是现代办公和通信中不可或缺的工具，它广泛应用于数据交换和工作沟通。为了更高效地处理邮件内容，我们可以借助程序来实现自动化处理。本文将详细介绍如何使用 Go 语言来接收和处理电子邮件。
通过查阅资料，了解到可以通过 IMAP 协议来接收电子邮件，IMAP 协议是电子邮件接收协议，它允许客户端通过网络连接到邮件服务器，并从服务器上下载邮件。除了 IMAP 协议，还有 POP3 协议，POP3 协议与 IMAP 协议类似，但它在在客户端上对邮件的操作不会反馈到邮件服务器上，也就是说，在客户端的操作不会影响服务器上的邮件。当你需要从多个邮件客户端访问邮件时，IMAP 协议是一个更好的选择。
go-imap 通过对比不同的库，最后选择了 go-imap 库，它是一个基于 IMAP 协议的 Go 语言库，可以通过它构建客户端或者服务端。
安装 可以通过以下命令安装：
go get github.com/emersion/go-imap 使用 我们将通过官方的例子进行切入：
先通过 DialTLS 连接对应的电子邮箱 IMAP 服务器，然后通过登录邮箱，获取所有的邮箱文件夹，最后选择收件箱，获取收件箱中最新的 4 封邮件，并打印没封邮件的主题。
运行代码：
2024/11/23 16:16:11 Connecting to server... 2024/11/23 16:16:11 Connected 2024/11/23 16:16:12 Logged in 2024/11/23 16:16:12 Mailboxes: 2024/11/23 16:16:13 \* 其他文件夹 2024/11/23 16:16:13 \* Drafts 2024/11/23 16:16:13 \* Deleted Messages 2024/11/23 16:16:13 \* Sent Messages 2024/11/23 16:16:13 \* Junk 2024/11/23 16:16:13 \* INBOX 2024/11/23 16:16:13 Flags for INBOX: \[\\Answered \\Flagged \\Deleted \\Draft \\Seen\] 2024/11/23 16:16:13 Last 4 messages: 2024/11/23 16:16:13 \* =?GBK?B?xx?= 2024/11/23 16:16:13 \* =?GBK?B?xxx?= 2024/11/23 16:16:13 \* =?GBK?B?xx==?= 2024/11/23 16:16:13 \* =?GBK?B?xx+k=?= 2024/11/23 16:16:13 Done! 可以看到打印出来的邮件主题是乱码，通过查询资料，了解到邮件的字段是采用特殊编码的，需要进行解码。可以通过 https://github.com/emersion/go-message 这个库进行解码。
...

 [post link to Go Recivie Email](https://jasminides.com/posts/go-recivie-email/)

前言 最近需要调用一个第三方的接口进行数据的采集，这个接口是基于 SOAP 协议的，所以需要使用 soap 相关的客户端进行调用。于是我调研了一些开源的 golang 的 soap 客户端，发现 go-soap 这个库的文档比较完善，而且使用起来也比较简单，所以就选择了这个库。
安装 使用以下命令进行安装：
go get github.com/tiaguinho/gosoap 使用 由于目前没有特别好的例子，这里就以官方的例子进行说明。
官方的代码如下：
package main import ( "encoding/xml" "log" "net/http" "time" "github.com/tiaguinho/gosoap" ) // GetIPLocationResponse will hold the Soap response type GetIPLocationResponse struct { GetIPLocationResult string \`xml:"GetIpLocationResult"\` } // GetIPLocationResult will type GetIPLocationResult struct { XMLName xml.Name \`xml:"GeoIP"\` Country string \`xml:"Country"\` State string \`xml:"State"\` } var ( r GetIPLocationResponse ) func main() { httpClient := &http.Client{ Timeout: 1500 \* time.Millisecond, } soap, err := gosoap.SoapClient("http://wsgeoip.lavasoft.com/ipservice.asmx?WSDL", httpClient) if err != nil { log.Fatalf("SoapClient error: %s", err) } // Use gosoap.ArrayParams to support fixed position params params := gosoap.Params{ "sIp": "8.8.8.8", } res, err := soap.Call("GetIpLocation", params) if err != nil { log.Fatalf("Call error: %s", err) } res.Unmarshal(&r) // GetIpLocationResult will be a string. We need to parse it to XML result := GetIPLocationResult{} err = xml.Unmarshal(\[\]byte(r.GetIPLocationResult), &result) if err != nil { log.Fatalf("xml.Unmarshal error: %s", err) } if result.Country != "US" { log.Fatalf("error: %+v", r) } log.Println("Country: ", result.Country) log.Println("State: ", result.State) } 可以看到 go-soap 的使用跟常规的 http client 的使用方法类似，都是创建一个连接，准备方法的参数，然后调用相应的方法。 这段代码展示了如何使用 go-soap 库连接 SOAP 服务、发送请求、处理响应，以及如何解析 XML 格式的返回数据。
...

 [post link to go-soap 简介](https://jasminides.com/posts/go-soap-desc/)

前言 最近遇到 Docker Desktop 构建 node 项目时，由于网络问题导致的构建失败问题，本文将介绍两个给 Docker Desktop 设置网络代理的方法。
修改 WSL2 配置 为了测试代理的效果，这里创建一个 go 服务，代码很简单，就是访问 https://www.google.com/ 并返回结果。如果能正常访问，说明代理设置成功。
package main import "net/http" func main() { resp, err := http.Get("https://www.google.com/") if err != nil { panic(err) } defer resp.Body.Close() println(resp.Status) } 第一种方法是修改 WSL2 的配置，在 windows C:\\Users<your\_username> 目录下创建 .wslconfig 文件，输入以下内容：
\[experimental\] autoMemoryReclaim=gradual networkingMode=mirrored dnsTunneling=true firewall=true autoProxy=true 然后重启 WSL: wsl --shutdown
networkingMode 为 mirrored 表示网络模式使用镜像模式，会镜像宿主机的网络设置，能更好的集成宿主机和 WSL 的网络。
autoProxy 开启了自动代理的功能，意味 WSL 自动配置代理设置。
配置好，我们构建 Docker 镜像，运行：
可以看到代理成功生效，可以正常访问。
...

 [post link to Docker Desktop 设置网络代理](https://jasminides.com/posts/docker-desktop-proxy/)

前言 本文将介绍当初我搭建这个博客网站的时候，是如何将 Hugo 网站部署到 GitHub 上的，本文会采用与 hugo 官方不同的方式进行部署。
创建仓库 首先我们在 GitHub 上创建一个仓库，仓库名称为 username.github.io，其中 username 为你的 GitHub 用户名。这个仓库是用来存储 hugo 最终生成的静态网站文件的。再创建一个名称为 blogs 的仓库，这个仓库是用来存储 hugo 网站源内容文件的。
启用 GitHub Pages 在 username.github.io 仓库中，点击 Settings 选项卡，在 GitHub Pages 中选择 Source 为 从分支部署，然后点击 Save 按钮。
启用 GitHub Actions 接下来要实现提交 hugo 网站源文件到 blogs 仓库后，自动将 hugo 网站源文件编译成静态网站文件，并提交到 username.github.io 仓库中，这样就可以通过访问 username.github.io 仓库来访问 hugo 网站了。
生成 personal\_token 在配置 Actions 前，需要先生成 personal\_token，用于在 GitHub Actions 中使用。我们进入 Settings 选项卡，在 Developer settings 中选择 Personal access tokens，然后选择 Tokens (classic)，然后点击 Generate new token 下的Generate new token(classic)按钮，在 Note 中输入 blog，在 Expiration 中选择 No expiration，在 Select scopes 中选择 repo 和 admin:repo\_hook，然后点击 Generate token 按钮，生成 personal\_token。
...

 [post link to 如何在 Github Pages 上部署 Hugo 网站](https://jasminides.com/posts/hugo_deploy_github/)

v0.dev chat 介绍 v0.dev chat 是 vercel 推出的最新的生成式 AI 聊天机器人，可以通过用户对话的方式来生成相应的 react 代码。
v0.dev chat 相比 V0.dev 有以下优点：
最新的 react、next.js、web 技术知识 可以运行 npm 包 更快更可靠的流失传输 接下来将通过官方的几个例子及个人尝试的效果来讲解。
官方例子 解释 next 缓存机制 打开 https://v0.dev/chat/E8fIPvg，可以看到 bot 很好的通过图表及文字讲述了 next 的缓存机制。
贪吃蛇游戏 打开这个 https://v0.dev/chat/AjJVzgx，可以看到用户上传蛇的皮肤并一步步引导 bot 生成贪吃蛇游戏。
个人尝试 接下来将通过一个简单的视频网站例子来尝试 v0.dev chat 的效果。
先通过简单的提示生成视频网站的初始代码： 可以看到 bot 生成的代码是非常完整的，并且可以运行预览的。接下来继续完善视频网站。
接下来添加视频下载保存功能 接下来添加视频网站首页功能 通过不断的调整，可以慢慢的形成一个视频网站的雏形。
总结 v0.dev chat 可以很好的通过对话的方式来生成 react 代码，并且可以运行 npm 包，可以很好的帮助我们快速生成代码。本文通过构建一个视频网站的例子来尝试 v0.dev，由于免费版限制了 message 的数量，感兴趣的可以自行尝试。视频网站的生成步骤可以通过此链接查看：https://v0.dev/chat/PsqNuwjpzXx
...

 [post link to V0.dev chat](https://jasminides.com/posts/v0dev/)

前言 最近需要写总结报告，以前写总结报告时，往往使用 Word 进行编写，但由于显示排版等问题，本次采用了 Markdown 进行编写，在编写时使用了 Markdown Preview Enhanced 插件。本文介绍 Markdown Preview Enhanced 插件的安装及所使用的功能。
安装 打开 vscode 编辑器，打开扩展栏，输入 Markdown Preview Enhanced ,第一个就是，点击安装后即可。
功能介绍 接下来将介绍一些在编写文档中所使用的功能。
diagrams Markdown Preview Enhanced 插件支持 low charts, sequence diagrams, mermaid, PlantUML, WaveDrom, GraphViz，Vega & Vega-lite，Ditaa 图像渲染。
在文档中我使用了 mermaid 和 Vega-lite，Vega-lite 用于绘制图表，mermaid 用于绘制流程图。
接下来介绍 markdown 中如何使用 Vega-lite 绘制图表，使用以下代码即可绘制一个漂亮的饼图：
如果想要居中的效果，可以添加 {align="center"}来设置居中的效果。
mermaid 可以用来绘制流程图，使用以下代码即可绘制一个简单的流程图：
如果我们想要添加 css 效果该怎么办呢，可以通过 HTML + css 的形式来显示我们想要的效果：
...

 [post link to Markdown Preview Enhanced plugin introduction and simple use](https://jasminides.com/posts/markdown-preview-enhanced/)

前言 今天在 Github 查看一些开源项目时，发现了一个"人性化"的项目 go-humanize，此项目可以将一些常见的容量、时间、千分位转换为人们可以理解的形式，例如一个文件大小是 2000000 bytes，我们不能很好的理解，但如果告诉你是 2mb，我们就能很好的理解了。go-humanize 就是方便的将一些不太能快速理解的数字转换为人们可以理解的形式。
安装 使用以下命令安装：
go get github.com/dustin/go-humanize 使用 接下来分别介绍一些常见的功能。
容量转换 现在我们有一个文件大小是 52854982 bytes，我们使用 humanize 包的 Bytes 方法将其转换为人们可以理解的形式 53MB，也可以使用 IBytes 方法转换为 MIB 单位的值。也可以使用 ParseBytes 方法将可以理解的形式转换为 bytes 单位的值。
fmt.Printf("That file is %s.\\n", humanize.IBytes(52854982)) fmt.Printf("That file is %s.", humanize.Bytes(52854982)) 时间转换 时间转换与容量转换类型，使用方法十分类似，使用方法如下：
t := time.Now().Add(time.Hour \* -7) fmt.Printf("This was touched %s.", humanize.Time(t)) //This was touched 7 hours ago. Time 根据相对时间转换为人们可以理解的形式，例如：xx 天之前、xx 小时之后等形式。
千分位转换 如果我们想在数字中添加逗号，就可以使用 Comma 方法，例如在处理金额时，我们通常会使用逗号将数字分隔开，例如 1,000,000,000
fmt.Printf("num is %s.", humanize.Comma(1000000000)) 还可以使用 Commaf 方法将浮点数转换为千分位形式。
位序 在日常使用中，我们有时需要表示位序例如 1st、2nd、3rd、4th 等，humanize 包也提供了相应的功能。
...

 [post link to go humanize 介绍](https://jasminides.com/posts/go-humanize-introduce-/) [Go to Top (Alt + G)](https://jasminides.com/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801865031&bpp=3&bdt=202&idt=141&shv=r20250319&mjsv=m202503190101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=339236796660&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95332587%2C95353451%2C31091178%2C95355964&oid=2&pvsid=433673636199121&tmod=204797395&uas=0&nvt=1&fsapi=1&fc=1920&brdim=260%2C260%2C260%2C260%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&pgls=CAA.&ifi=1&uci=a!1&fsb=1&dtd=166)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## AI Tools Overview
前言 前段时间看到了一个项目 mi-gpt ,可以将你的小爱音箱接入 gpt，改造成专属于你的语音助手。
接下来就由作者来介绍小爱同学从零接入 deepseek 的过程。
设置环境变量和配置文件 mi-gpt 有两种部署方式，一是使用 docker 部署，二是使用 Node.js 进行部署，本文使用 docker 进行部署使用。
需要提供两个文件 .env 和 .migpt.js 文件，.migpt.js 是配置文件，包括一些配置，.env 是环境变量文件，存放 gpt 密钥相关文件。文件的例子可以从仓库里复制，然后进行相应的修改。
启动 使用以下命令启动 docker:
docker run -d --env-file $(pwd)/.env -v $(pwd)/.migpt.js:/app/.migpt.js idootop/mi-gpt:latest windows 环境下需要将$(pwd) 替换为绝对路径。
启动后可以通过 callAIKeywords 设置的关键字调用 ai 来响应用户的消息。
小结 本文介绍了使用 mi-gpt 升级你的闲置的小爱音箱，通过简单的测试和使用，个人感觉还不够完善，稳定性不够好，感兴趣的读者可以根据本文的内容进行自行搭建尝试。
参考 https://github.com/idootop/mi-gpt

 [post link to 使用 gpt 改造你的小米音箱](https://jasminides.com/posts/mi_gpt/)

v0.dev chat 介绍 v0.dev chat 是 vercel 推出的最新的生成式 AI 聊天机器人，可以通过用户对话的方式来生成相应的 react 代码。
v0.dev chat 相比 V0.dev 有以下优点：
最新的 react、next.js、web 技术知识 可以运行 npm 包 更快更可靠的流失传输 接下来将通过官方的几个例子及个人尝试的效果来讲解。
官方例子 解释 next 缓存机制 打开 https://v0.dev/chat/E8fIPvg，可以看到 bot 很好的通过图表及文字讲述了 next 的缓存机制。
贪吃蛇游戏 打开这个 https://v0.dev/chat/AjJVzgx，可以看到用户上传蛇的皮肤并一步步引导 bot 生成贪吃蛇游戏。
个人尝试 接下来将通过一个简单的视频网站例子来尝试 v0.dev chat 的效果。
先通过简单的提示生成视频网站的初始代码： 可以看到 bot 生成的代码是非常完整的，并且可以运行预览的。接下来继续完善视频网站。
接下来添加视频下载保存功能 接下来添加视频网站首页功能 通过不断的调整，可以慢慢的形成一个视频网站的雏形。
总结 v0.dev chat 可以很好的通过对话的方式来生成 react 代码，并且可以运行 npm 包，可以很好的帮助我们快速生成代码。本文通过构建一个视频网站的例子来尝试 v0.dev，由于免费版限制了 message 的数量，感兴趣的可以自行尝试。视频网站的生成步骤可以通过此链接查看：https://v0.dev/chat/PsqNuwjpzXx
...

 [post link to V0.dev chat](https://jasminides.com/posts/v0dev/)

介绍 cody 是一个 AI 编程助手，可以帮助你更快更好的理解代码，编写代码，解决代码中的问题。通过本地代码仓库和远程代码库提取上下文，让你能够更好的理解和编写代码。Cody 目前可以在以下编程工具中使用:
VS Code JetBrains IDE Neovim (实验性) Web (实验性) Cody 主要有以下功能:
自动完成 基于代码上下文的自动补全 聊天 在聊天视图中询问代码相关的问题 命令 为常见的操作提供了快捷命令，例如：生成文档，添加测试，检测代码问题 调试 在编辑器中调试代码，帮你寻找代码中的问题 忽略 可以过滤某些文件及过滤某些仓库 价格 介绍完 Cody 的特点后，接下来介绍大家关心的价格问题，Cody 有 3 个版本，分别是 Free、Pro、Enterprise.
Free 版本为免费版，目前每月提供 20 次聊天次数、500 次代码自动完成，今天查看 sourcegraph 的 blog，发现 Free 版本的额度提高了，代码自动完成次数为无限次，聊天和命令次数增加了 10 倍为 200 次。
Pro 版本为每个月 9 美元，提供了不限次数的代码补全及聊天功能及提供了 GPT-4o 等高级 LLM.
Enterprise 的价格需要联系 sourcegraph 的销售人员，Enterprise 相较于 Pro 版提供了更多的团队功能。
安装 接下来介绍如何安装 Cody，主要介绍 VS Code 中如何安装：
...

 [post link to AI 编程助手 - Cody](https://jasminides.com/posts/cody/)

magika 介绍 Magika 是 Google 推出的一个新型工具，使用 AI 用来文件类型的检测，采用了高度优化的 Keras 模型，具有较高的准确性、模型较小等优点，支持100多种文件类型，准确性高达 99%,推测每个文件的时间大约 5 ms。
Magika 在 Google 内部已被大量使用，用于 Gmail，网络硬盘等应用，检测各种文件，提高了用户的安全性。
Magika 提供了 Pyhton 命令行、Pyhton API 和 js 包等多种方式使用，还支持批量处理提高推理速度。
安装 可以使用 pip 命令进行安装：pip install magika
如果没有 Python 环境，还可以 Docker 中进行使用：
git clone https://github.com/google/magika cd magika/ docker build -t magika . docker run -it --rm -v $(pwd):/magika magika -r /magika/tests\_data 如果 Docker 环境也没有，那你可以使用 Google 部署的网站进行试用 https://google.github.io/magika/。
运行 运行仓库提供的测试数据 (magika -r /magika/tests\_data): 可以看到文件的类型很精准的被识别出来了。
接下来做个试验，将一个 png 的图片的后缀修改为 jpg ,看看还能否正确识别，可以看到还是成功精准识别了。
...

 [post link to AI 检测文件类型 Magika](https://jasminides.com/posts/magika/)

前言 最近我发现各个群里出现了一股利用 AI 进行绘画的潮流，今天我也尝试使用 Stable Diffusion 模型 进行 AI 绘画。
Stable Diffusion 简介 Stable Diffusion 是一个文本到图像的模型，将使人们可以在几秒钟内创造出令人惊叹的艺术作品。它在速度和质量方面都有突破，这意味着它可以在消费级 GPU 上运行
开始 我们采用别人封装的 stable-diffusion-webui 平台进行绘画，由于各种条件限制，我们使用 github 上提供的 Google colab notbook 进行部署 (https://colab.research.google.com/drive/1IplUv47g9CgtlJmFnyT2sDyNYDEeMJDi?usp=sharing).
打开链接，我简单的看了下代码，前面是基础的安装运行环境、需要的 Python package .我们依次运行即可。
我们直接来到 1.4 Connect to Google Drive， 勾选 download\_if\_missing，然后到 https://huggingface.co/settings/tokens 复制你的 toekn 并填入。(huggingface 注册耗费了许多时间，reCAPTCHA 没有通过).
点击运行后就开始拉取模型。
如果运行发现报错了：
remote: Access to model CompVis/stable-diffusion-v-1-4-original is restricted and you are not in the authorized list. Visit https://huggingface.co/CompVis/stable-diffusion-v-1-4-original to ask for access. fatal: unable to access 'https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/': The requested URL returned error: 403 你需要到 https://huggingface.co/CompVis/stable-diffusion-v-1-4-original 授权模型的访问权限。授权后重新运行即可。
...

 [post link to AI 绘画初体验](https://jasminides.com/posts/ai%E7%BB%98%E7%94%BB%E5%88%9D%E4%BD%93%E9%AA%8C/) [Go to Top (Alt + G)](https://jasminides.com/tags/ai/#top "Go to Top (Alt + G)")

## Programming Solutions and Tutorials
前言 前段时间看到了一个项目 mi-gpt ,可以将你的小爱音箱接入 gpt，改造成专属于你的语音助手。
接下来就由作者来介绍小爱同学从零接入 deepseek 的过程。
设置环境变量和配置文件 mi-gpt 有两种部署方式，一是使用 docker 部署，二是使用 Node.js 进行部署，本文使用 docker 进行部署使用。
需要提供两个文件 .env 和 .migpt.js 文件，.migpt.js 是配置文件，包括一些配置，.env 是环境变量文件，存放 gpt 密钥相关文件。文件的例子可以从仓库里复制，然后进行相应的修改。
启动 使用以下命令启动 docker:
docker run -d --env-file $(pwd)/.env -v $(pwd)/.migpt.js:/app/.migpt.js idootop/mi-gpt:latest windows 环境下需要将$(pwd) 替换为绝对路径。
启动后可以通过 callAIKeywords 设置的关键字调用 ai 来响应用户的消息。
小结 本文介绍了使用 mi-gpt 升级你的闲置的小爱音箱，通过简单的测试和使用，个人感觉还不够完善，稳定性不够好，感兴趣的读者可以根据本文的内容进行自行搭建尝试。
参考 https://github.com/idootop/mi-gpt

 [post link to 使用 gpt 改造你的小米音箱](https://jasminides.com/posts/mi_gpt/)

前言 今天在编译构建一个 node.js 项目时，在构建过程中遇到了一些问题，本文将记录问题及对应的解决方案。
问题 1 在执行 npm run build 遇到此提示：
error Expected linebreaks to be 'LF' but found 'CRLF' linebreak-style 根据信息可以看出是 eslint 的报错，查看 .eslintrc.js 文件，修改 linebreak-style 对应的行：
'linebreak-style': \['error', process.platform === 'win32' ? 'windows' : 'unix'\], 重新运行命令，顺利构建成功。
这个问题的原因是项目的作者可能是使用 Linux 或 Mac 构建的，没有考虑 Windows 的情况，通过这行配置，可以根据运行的环境来决定 lint 规则。
问题 2 在执行 npm start 遇到了第二个问题：
Generating browser application bundles (phase: building)...node:internal/crypto/hash:79 this\[kHandle\] = new \_Hash(algorithm, xofLen, algorithmId, getHashCache()); ^ Error: error:0308010C:digital envelope routines::unsupported at new Hash (node:internal/crypto/hash:79:19) at Object.createHash (node:crypto:139:10) at BulkUpdateDecorator.hashFactory (D:\\code\\xx\\node\_modules\\webpack\\lib\\util\\createHash.js:145:18) at BulkUpdateDecorator.update (D:\\code\\xx\\node\_modules\\webpack\\lib\\util\\createHash.js:46:50) at RawSource.updateHash (D:\\code\\xx\\node\_modules\\webpack\\node\_modules\\webpack-sources\\lib\\RawSource.js:77:8) at NormalModule.\_initBuildHash (D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:880:17) at handleParseResult (D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:946:10) at D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:1040:4 at processResult (D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:755:11) at D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:819:5 { opensslErrorStack: \[ 'error:03000086:digital envelope routines::initialization error', 'error:0308010C:digital envelope routines::unsupported' \], library: 'digital envelope routines', reason: 'unsupported', code: 'ERR\_OSSL\_EVP\_UNSUPPORTED' } 根据这个报错，推测可能是啥 hash 算法不支持，通过查阅相关资料，得到以下解决方案：
...

 [post link to node.js 项目构建问题及解决](https://jasminides.com/posts/node_build_error/)

问题 最近在使用 go 解析 csv 文件时，读取并打印 csv 的每行内容时，读取到第 11 行时，程序报错，提示：
record on line 11: wrong number of fields 分析 遇到这个问题，我第一反应是 csv 文件的格式有问题，于是我使用 cat 命令查看 csv 文件，发现 csv 文件的格式是正确的，没有问题。 并查看分隔符是正确的，于是可以得出 csv 文件是没有问题的。
接下来就查看所使用的标准库 encoding/csv，通过查阅文档及 issue, 发现 csv 包中的 FieldsPerRecord 字段，FieldsPerRecord 表示 csv 文件每行的预期字段数， 如果为正数，则读取的每条记录都必须有对应的字段数，如果为 0，则会以第一条记录的数量为标准，接下来每行都必须有对应的字段数，如果为负数，则不会检查字段数。
修改后的代码如下：
package main import ( "encoding/csv" "fmt" "io" "log" "os" ) func main() { file, err := os.Open("./xx.csv") if err != nil { log.Fatal(err) } defer file.Close() // 创建一个 CSV reader reader := csv.NewReader(file) reader.FieldsPerRecord = -1 // 循环读取 CSV 文件中的每一行数据 for { record, err := reader.Read() if err == io.EOF { break } if err != nil { log.Fatal(err) } // 处理每一行数据 fmt.Println(record) fmt.Println(len(record)) } } 小结 本文记录了在使用 go 解析 csv 时遇到字段数不匹配的问题，并分析了问题的原因，并给出了相应的解决方法。
...

 [post link to go 解析 csv 文件报错](https://jasminides.com/posts/read_csv_error/)

前言 电子邮件是现代办公和通信中不可或缺的工具，它广泛应用于数据交换和工作沟通。为了更高效地处理邮件内容，我们可以借助程序来实现自动化处理。本文将详细介绍如何使用 Go 语言来接收和处理电子邮件。
通过查阅资料，了解到可以通过 IMAP 协议来接收电子邮件，IMAP 协议是电子邮件接收协议，它允许客户端通过网络连接到邮件服务器，并从服务器上下载邮件。除了 IMAP 协议，还有 POP3 协议，POP3 协议与 IMAP 协议类似，但它在在客户端上对邮件的操作不会反馈到邮件服务器上，也就是说，在客户端的操作不会影响服务器上的邮件。当你需要从多个邮件客户端访问邮件时，IMAP 协议是一个更好的选择。
go-imap 通过对比不同的库，最后选择了 go-imap 库，它是一个基于 IMAP 协议的 Go 语言库，可以通过它构建客户端或者服务端。
安装 可以通过以下命令安装：
go get github.com/emersion/go-imap 使用 我们将通过官方的例子进行切入：
先通过 DialTLS 连接对应的电子邮箱 IMAP 服务器，然后通过登录邮箱，获取所有的邮箱文件夹，最后选择收件箱，获取收件箱中最新的 4 封邮件，并打印没封邮件的主题。
运行代码：
2024/11/23 16:16:11 Connecting to server... 2024/11/23 16:16:11 Connected 2024/11/23 16:16:12 Logged in 2024/11/23 16:16:12 Mailboxes: 2024/11/23 16:16:13 \* 其他文件夹 2024/11/23 16:16:13 \* Drafts 2024/11/23 16:16:13 \* Deleted Messages 2024/11/23 16:16:13 \* Sent Messages 2024/11/23 16:16:13 \* Junk 2024/11/23 16:16:13 \* INBOX 2024/11/23 16:16:13 Flags for INBOX: \[\\Answered \\Flagged \\Deleted \\Draft \\Seen\] 2024/11/23 16:16:13 Last 4 messages: 2024/11/23 16:16:13 \* =?GBK?B?xx?= 2024/11/23 16:16:13 \* =?GBK?B?xxx?= 2024/11/23 16:16:13 \* =?GBK?B?xx==?= 2024/11/23 16:16:13 \* =?GBK?B?xx+k=?= 2024/11/23 16:16:13 Done! 可以看到打印出来的邮件主题是乱码，通过查询资料，了解到邮件的字段是采用特殊编码的，需要进行解码。可以通过 https://github.com/emersion/go-message 这个库进行解码。
...

 [post link to Go Recivie Email](https://jasminides.com/posts/go-recivie-email/)

前言 最近需要调用一个第三方的接口进行数据的采集，这个接口是基于 SOAP 协议的，所以需要使用 soap 相关的客户端进行调用。于是我调研了一些开源的 golang 的 soap 客户端，发现 go-soap 这个库的文档比较完善，而且使用起来也比较简单，所以就选择了这个库。
安装 使用以下命令进行安装：
go get github.com/tiaguinho/gosoap 使用 由于目前没有特别好的例子，这里就以官方的例子进行说明。
官方的代码如下：
package main import ( "encoding/xml" "log" "net/http" "time" "github.com/tiaguinho/gosoap" ) // GetIPLocationResponse will hold the Soap response type GetIPLocationResponse struct { GetIPLocationResult string \`xml:"GetIpLocationResult"\` } // GetIPLocationResult will type GetIPLocationResult struct { XMLName xml.Name \`xml:"GeoIP"\` Country string \`xml:"Country"\` State string \`xml:"State"\` } var ( r GetIPLocationResponse ) func main() { httpClient := &http.Client{ Timeout: 1500 \* time.Millisecond, } soap, err := gosoap.SoapClient("http://wsgeoip.lavasoft.com/ipservice.asmx?WSDL", httpClient) if err != nil { log.Fatalf("SoapClient error: %s", err) } // Use gosoap.ArrayParams to support fixed position params params := gosoap.Params{ "sIp": "8.8.8.8", } res, err := soap.Call("GetIpLocation", params) if err != nil { log.Fatalf("Call error: %s", err) } res.Unmarshal(&r) // GetIpLocationResult will be a string. We need to parse it to XML result := GetIPLocationResult{} err = xml.Unmarshal(\[\]byte(r.GetIPLocationResult), &result) if err != nil { log.Fatalf("xml.Unmarshal error: %s", err) } if result.Country != "US" { log.Fatalf("error: %+v", r) } log.Println("Country: ", result.Country) log.Println("State: ", result.State) } 可以看到 go-soap 的使用跟常规的 http client 的使用方法类似，都是创建一个连接，准备方法的参数，然后调用相应的方法。 这段代码展示了如何使用 go-soap 库连接 SOAP 服务、发送请求、处理响应，以及如何解析 XML 格式的返回数据。
...

 [post link to go-soap 简介](https://jasminides.com/posts/go-soap-desc/)

前言 最近遇到 Docker Desktop 构建 node 项目时，由于网络问题导致的构建失败问题，本文将介绍两个给 Docker Desktop 设置网络代理的方法。
修改 WSL2 配置 为了测试代理的效果，这里创建一个 go 服务，代码很简单，就是访问 https://www.google.com/ 并返回结果。如果能正常访问，说明代理设置成功。
package main import "net/http" func main() { resp, err := http.Get("https://www.google.com/") if err != nil { panic(err) } defer resp.Body.Close() println(resp.Status) } 第一种方法是修改 WSL2 的配置，在 windows C:\\Users<your\_username> 目录下创建 .wslconfig 文件，输入以下内容：
\[experimental\] autoMemoryReclaim=gradual networkingMode=mirrored dnsTunneling=true firewall=true autoProxy=true 然后重启 WSL: wsl --shutdown
networkingMode 为 mirrored 表示网络模式使用镜像模式，会镜像宿主机的网络设置，能更好的集成宿主机和 WSL 的网络。
autoProxy 开启了自动代理的功能，意味 WSL 自动配置代理设置。
配置好，我们构建 Docker 镜像，运行：
可以看到代理成功生效，可以正常访问。
...

 [post link to Docker Desktop 设置网络代理](https://jasminides.com/posts/docker-desktop-proxy/)

前言 本文将介绍当初我搭建这个博客网站的时候，是如何将 Hugo 网站部署到 GitHub 上的，本文会采用与 hugo 官方不同的方式进行部署。
创建仓库 首先我们在 GitHub 上创建一个仓库，仓库名称为 username.github.io，其中 username 为你的 GitHub 用户名。这个仓库是用来存储 hugo 最终生成的静态网站文件的。再创建一个名称为 blogs 的仓库，这个仓库是用来存储 hugo 网站源内容文件的。
启用 GitHub Pages 在 username.github.io 仓库中，点击 Settings 选项卡，在 GitHub Pages 中选择 Source 为 从分支部署，然后点击 Save 按钮。
启用 GitHub Actions 接下来要实现提交 hugo 网站源文件到 blogs 仓库后，自动将 hugo 网站源文件编译成静态网站文件，并提交到 username.github.io 仓库中，这样就可以通过访问 username.github.io 仓库来访问 hugo 网站了。
生成 personal\_token 在配置 Actions 前，需要先生成 personal\_token，用于在 GitHub Actions 中使用。我们进入 Settings 选项卡，在 Developer settings 中选择 Personal access tokens，然后选择 Tokens (classic)，然后点击 Generate new token 下的Generate new token(classic)按钮，在 Note 中输入 blog，在 Expiration 中选择 No expiration，在 Select scopes 中选择 repo 和 admin:repo\_hook，然后点击 Generate token 按钮，生成 personal\_token。
...

 [post link to 如何在 Github Pages 上部署 Hugo 网站](https://jasminides.com/posts/hugo_deploy_github/)

v0.dev chat 介绍 v0.dev chat 是 vercel 推出的最新的生成式 AI 聊天机器人，可以通过用户对话的方式来生成相应的 react 代码。
v0.dev chat 相比 V0.dev 有以下优点：
最新的 react、next.js、web 技术知识 可以运行 npm 包 更快更可靠的流失传输 接下来将通过官方的几个例子及个人尝试的效果来讲解。
官方例子 解释 next 缓存机制 打开 https://v0.dev/chat/E8fIPvg，可以看到 bot 很好的通过图表及文字讲述了 next 的缓存机制。
贪吃蛇游戏 打开这个 https://v0.dev/chat/AjJVzgx，可以看到用户上传蛇的皮肤并一步步引导 bot 生成贪吃蛇游戏。
个人尝试 接下来将通过一个简单的视频网站例子来尝试 v0.dev chat 的效果。
先通过简单的提示生成视频网站的初始代码： 可以看到 bot 生成的代码是非常完整的，并且可以运行预览的。接下来继续完善视频网站。
接下来添加视频下载保存功能 接下来添加视频网站首页功能 通过不断的调整，可以慢慢的形成一个视频网站的雏形。
总结 v0.dev chat 可以很好的通过对话的方式来生成 react 代码，并且可以运行 npm 包，可以很好的帮助我们快速生成代码。本文通过构建一个视频网站的例子来尝试 v0.dev，由于免费版限制了 message 的数量，感兴趣的可以自行尝试。视频网站的生成步骤可以通过此链接查看：https://v0.dev/chat/PsqNuwjpzXx
...

 [post link to V0.dev chat](https://jasminides.com/posts/v0dev/)

前言 最近需要写总结报告，以前写总结报告时，往往使用 Word 进行编写，但由于显示排版等问题，本次采用了 Markdown 进行编写，在编写时使用了 Markdown Preview Enhanced 插件。本文介绍 Markdown Preview Enhanced 插件的安装及所使用的功能。
安装 打开 vscode 编辑器，打开扩展栏，输入 Markdown Preview Enhanced ,第一个就是，点击安装后即可。
功能介绍 接下来将介绍一些在编写文档中所使用的功能。
diagrams Markdown Preview Enhanced 插件支持 low charts, sequence diagrams, mermaid, PlantUML, WaveDrom, GraphViz，Vega & Vega-lite，Ditaa 图像渲染。
在文档中我使用了 mermaid 和 Vega-lite，Vega-lite 用于绘制图表，mermaid 用于绘制流程图。
接下来介绍 markdown 中如何使用 Vega-lite 绘制图表，使用以下代码即可绘制一个漂亮的饼图：
如果想要居中的效果，可以添加 {align="center"}来设置居中的效果。
mermaid 可以用来绘制流程图，使用以下代码即可绘制一个简单的流程图：
如果我们想要添加 css 效果该怎么办呢，可以通过 HTML + css 的形式来显示我们想要的效果：
...

 [post link to Markdown Preview Enhanced plugin introduction and simple use](https://jasminides.com/posts/markdown-preview-enhanced/)

前言 今天在 Github 查看一些开源项目时，发现了一个"人性化"的项目 go-humanize，此项目可以将一些常见的容量、时间、千分位转换为人们可以理解的形式，例如一个文件大小是 2000000 bytes，我们不能很好的理解，但如果告诉你是 2mb，我们就能很好的理解了。go-humanize 就是方便的将一些不太能快速理解的数字转换为人们可以理解的形式。
安装 使用以下命令安装：
go get github.com/dustin/go-humanize 使用 接下来分别介绍一些常见的功能。
容量转换 现在我们有一个文件大小是 52854982 bytes，我们使用 humanize 包的 Bytes 方法将其转换为人们可以理解的形式 53MB，也可以使用 IBytes 方法转换为 MIB 单位的值。也可以使用 ParseBytes 方法将可以理解的形式转换为 bytes 单位的值。
fmt.Printf("That file is %s.\\n", humanize.IBytes(52854982)) fmt.Printf("That file is %s.", humanize.Bytes(52854982)) 时间转换 时间转换与容量转换类型，使用方法十分类似，使用方法如下：
t := time.Now().Add(time.Hour \* -7) fmt.Printf("This was touched %s.", humanize.Time(t)) //This was touched 7 hours ago. Time 根据相对时间转换为人们可以理解的形式，例如：xx 天之前、xx 小时之后等形式。
千分位转换 如果我们想在数字中添加逗号，就可以使用 Comma 方法，例如在处理金额时，我们通常会使用逗号将数字分隔开，例如 1,000,000,000
fmt.Printf("num is %s.", humanize.Comma(1000000000)) 还可以使用 Commaf 方法将浮点数转换为千分位形式。
位序 在日常使用中，我们有时需要表示位序例如 1st、2nd、3rd、4th 等，humanize 包也提供了相应的功能。
...

 [post link to go humanize 介绍](https://jasminides.com/posts/go-humanize-introduce-/) [Go to Top (Alt + G)](https://jasminides.com/posts/#top "Go to Top (Alt + G)")

## Technology Tags
- [413 **1**](https://jasminides.com/tags/413/)
- [acme.sh **1**](https://jasminides.com/tags/acme.sh/)
- [adsense **1**](https://jasminides.com/tags/adsense/)
- [AES **1**](https://jasminides.com/tags/aes/)
- [AI **5**](https://jasminides.com/tags/ai/)
- [aliyun **1**](https://jasminides.com/tags/aliyun/)
- [apisix **12**](https://jasminides.com/tags/apisix/)
- [zip **1**](https://jasminides.com/tags/archive/zip/)
- [atop **1**](https://jasminides.com/tags/atop/)
- [authing **1**](https://jasminides.com/tags/authing/)
- [Bot **1**](https://jasminides.com/tags/bot/)
- [buf **2**](https://jasminides.com/tags/buf/)
- [casbin **1**](https://jasminides.com/tags/casbin/)
- [cdn **2**](https://jasminides.com/tags/cdn/)
- [cert-manager **1**](https://jasminides.com/tags/cert-manager/)
- [CertificateManager **1**](https://jasminides.com/tags/certificatemanager/)
- [chrome **1**](https://jasminides.com/tags/chrome/)
- [CI **1**](https://jasminides.com/tags/ci/)
- [clarity **1**](https://jasminides.com/tags/clarity/)
- [clean cache **1**](https://jasminides.com/tags/clean-cache/)
- [Cody **1**](https://jasminides.com/tags/cody/)
- [colab **1**](https://jasminides.com/tags/colab/)
- [conc **1**](https://jasminides.com/tags/conc/)
- [concurrency **1**](https://jasminides.com/tags/concurrency/)
- [ConfigMaps **1**](https://jasminides.com/tags/configmaps/)
- [consul **1**](https://jasminides.com/tags/consul/)
- [containerd **3**](https://jasminides.com/tags/containerd/)
- [coverage **1**](https://jasminides.com/tags/coverage/)
- [coze **1**](https://jasminides.com/tags/coze/)
- [cpu **2**](https://jasminides.com/tags/cpu/)
- [Crash **1**](https://jasminides.com/tags/crash/)
- [crawler **1**](https://jasminides.com/tags/crawler/)
- [crypto **1**](https://jasminides.com/tags/crypto/)
- [csv **1**](https://jasminides.com/tags/csv/)
- [CTE **1**](https://jasminides.com/tags/cte/)
- [CVE-2021-22205 **1**](https://jasminides.com/tags/cve-2021-22205/)
- [data-visualization **1**](https://jasminides.com/tags/data-visualization/)
- [database **1**](https://jasminides.com/tags/database/)
- [DataX **1**](https://jasminides.com/tags/datax/)
- [date **1**](https://jasminides.com/tags/date/)
- [decode **1**](https://jasminides.com/tags/decode/)
- [dms **1**](https://jasminides.com/tags/dms/)
- [DNS **1**](https://jasminides.com/tags/dns/)
- [DNS authorization **1**](https://jasminides.com/tags/dns-authorization/)
- [docker **8**](https://jasminides.com/tags/docker/)
- [Easeprobe **1**](https://jasminides.com/tags/easeprobe/)
- [email **1**](https://jasminides.com/tags/email/)
- [embed **1**](https://jasminides.com/tags/embed/)
- [ent **1**](https://jasminides.com/tags/ent/)
- [errgroup **1**](https://jasminides.com/tags/errgroup/)
- [error **1**](https://jasminides.com/tags/error/)
- [external **1**](https://jasminides.com/tags/external/)
- [ffmpeg **1**](https://jasminides.com/tags/ffmpeg/)
- [Finalizers **1**](https://jasminides.com/tags/finalizers/)
- [Fly.io **3**](https://jasminides.com/tags/fly.io/)
- [fsck **1**](https://jasminides.com/tags/fsck/)
- [gcloud **1**](https://jasminides.com/tags/gcloud/)
- [gin **1**](https://jasminides.com/tags/gin/)
- [Github **1**](https://jasminides.com/tags/github/)
- [GitHub Pages **1**](https://jasminides.com/tags/github-pages/)
- [gitlab **2**](https://jasminides.com/tags/gitlab/)
- [go **50**](https://jasminides.com/tags/go/)
- [golang **22**](https://jasminides.com/tags/golang/)
- [gonew **1**](https://jasminides.com/tags/gonew/)
- [google **1**](https://jasminides.com/tags/google/)
- [Google analytics **1**](https://jasminides.com/tags/google-analytics/)
- [google api **1**](https://jasminides.com/tags/google-api/)
- [google cloud **1**](https://jasminides.com/tags/google-cloud/)
- [google\_OAuth2 **1**](https://jasminides.com/tags/google_oauth2/)
- [govulncheck **1**](https://jasminides.com/tags/govulncheck/)
- [grafana **1**](https://jasminides.com/tags/grafana/)
- [gRPC **14**](https://jasminides.com/tags/grpc/)
- [gzip **1**](https://jasminides.com/tags/gzip/)
- [health check **1**](https://jasminides.com/tags/health-check/)
- [Helm **1**](https://jasminides.com/tags/helm/)
- [hosts **1**](https://jasminides.com/tags/hosts/)
- [HTTP **1**](https://jasminides.com/tags/http/)
- [https **3**](https://jasminides.com/tags/https/)
- [hugo **1**](https://jasminides.com/tags/hugo/)
- [humanize **1**](https://jasminides.com/tags/humanize/)
- [i18n **1**](https://jasminides.com/tags/i18n/)
- [image compress **1**](https://jasminides.com/tags/image-compress/)
- [imap **1**](https://jasminides.com/tags/imap/)
- [init **1**](https://jasminides.com/tags/init/)
- [json **2**](https://jasminides.com/tags/json/)
- [k8s **2**](https://jasminides.com/tags/k8s/)
- [katana **1**](https://jasminides.com/tags/katana/)
- [kratos **2**](https://jasminides.com/tags/kratos/)
- [kubernetes **13**](https://jasminides.com/tags/kubernetes/)
- [lint **2**](https://jasminides.com/tags/lint/)
- [linter **1**](https://jasminides.com/tags/linter/)
- [Linux **4**](https://jasminides.com/tags/linux/)
- [load\_balancing **1**](https://jasminides.com/tags/load_balancing/)
- [log **1**](https://jasminides.com/tags/log/)
- [loki **1**](https://jasminides.com/tags/loki/)
- [lua **1**](https://jasminides.com/tags/lua/)
- [Magika **1**](https://jasminides.com/tags/magika/)
- [mapping **1**](https://jasminides.com/tags/mapping/)
- [markdown **1**](https://jasminides.com/tags/markdown/)
- [memory **1**](https://jasminides.com/tags/memory/)
- [mergo **1**](https://jasminides.com/tags/mergo/)
- [metabase **1**](https://jasminides.com/tags/metabase/)
- [microsoft **1**](https://jasminides.com/tags/microsoft/)
- [MinIO **4**](https://jasminides.com/tags/minio/)
- [monitor **3**](https://jasminides.com/tags/monitor/)
- [nginx **5**](https://jasminides.com/tags/nginx/)
- [nginx ingress **1**](https://jasminides.com/tags/nginx-ingress/)
- [node.js **2**](https://jasminides.com/tags/node.js/)
- [NovelAI **1**](https://jasminides.com/tags/novelai/)
- [oauth2 **1**](https://jasminides.com/tags/oauth2/)
- [once **1**](https://jasminides.com/tags/once/)
- [OpenTelemetry **2**](https://jasminides.com/tags/opentelemetry/)
- [OpenTracing **1**](https://jasminides.com/tags/opentracing/)
- [openwrite **1**](https://jasminides.com/tags/openwrite/)
- [os **1**](https://jasminides.com/tags/os/)
- [PaaS **1**](https://jasminides.com/tags/paas/)
- [performance **2**](https://jasminides.com/tags/performance/)
- [playwright **1**](https://jasminides.com/tags/playwright/)
- [playwright-go **1**](https://jasminides.com/tags/playwright-go/)
- [plugin **2**](https://jasminides.com/tags/plugin/)
- [png **2**](https://jasminides.com/tags/png/)
- [pngcrush **1**](https://jasminides.com/tags/pngcrush/)
- [pngquant **1**](https://jasminides.com/tags/pngquant/)
- [PostgreSQL **6**](https://jasminides.com/tags/postgresql/)
- [profiling **2**](https://jasminides.com/tags/profiling/)
- [Prometheus **2**](https://jasminides.com/tags/prometheus/)
- [protobuf **2**](https://jasminides.com/tags/protobuf/)
- [proxy **2**](https://jasminides.com/tags/proxy/)
- [psutil **1**](https://jasminides.com/tags/psutil/)
- [pyroscope **1**](https://jasminides.com/tags/pyroscope/)
- [rancher **2**](https://jasminides.com/tags/rancher/)
- [rand **1**](https://jasminides.com/tags/rand/)
- [redis **2**](https://jasminides.com/tags/redis/)
- [retry **1**](https://jasminides.com/tags/retry/)
- [Reverse Proxy **1**](https://jasminides.com/tags/reverse-proxy/)
- [rueidis **1**](https://jasminides.com/tags/rueidis/)
- [sealos **2**](https://jasminides.com/tags/sealos/)
- [security **1**](https://jasminides.com/tags/security/)
- [server reflection **1**](https://jasminides.com/tags/server-reflection/)
- [serverless **1**](https://jasminides.com/tags/serverless/)
- [service **2**](https://jasminides.com/tags/service/)
- [singleflight **1**](https://jasminides.com/tags/singleflight/)
- [slug **1**](https://jasminides.com/tags/slug/)
- [soap **1**](https://jasminides.com/tags/soap/)
- [spider **1**](https://jasminides.com/tags/spider/)
- [sql **3**](https://jasminides.com/tags/sql/)
- [sqlc **1**](https://jasminides.com/tags/sqlc/)
- [Stable Diffusion **1**](https://jasminides.com/tags/stable-diffusion/)
- [storage **1**](https://jasminides.com/tags/storage/)
- [Superset **1**](https://jasminides.com/tags/superset/)
- [swap **2**](https://jasminides.com/tags/swap/)
- [sync **1**](https://jasminides.com/tags/sync/)
- [UDP **1**](https://jasminides.com/tags/tcp/udp/)
- [template **2**](https://jasminides.com/tags/template/)
- [test **1**](https://jasminides.com/tags/test/)
- [text **1**](https://jasminides.com/tags/text/)
- [Tianji **1**](https://jasminides.com/tags/tianji/)
- [time **1**](https://jasminides.com/tags/time/)
- [TLS **1**](https://jasminides.com/tags/tls/)
- [trace **3**](https://jasminides.com/tags/trace/)
- [trace-viewer **2**](https://jasminides.com/tags/trace-viewer/)
- [Traefik **1**](https://jasminides.com/tags/traefik/)
- [Ubuntu **2**](https://jasminides.com/tags/ubuntu/)
- [uri **1**](https://jasminides.com/tags/uri/)
- [v0.dev **1**](https://jasminides.com/tags/v0.dev/)
- [video **1**](https://jasminides.com/tags/video/)
- [visualization **1**](https://jasminides.com/tags/visualization/)
- [visualstudio **1**](https://jasminides.com/tags/visualstudio/)
- [wasi **1**](https://jasminides.com/tags/wasi/)
- [wasm **2**](https://jasminides.com/tags/wasm/)
- [Wire **1**](https://jasminides.com/tags/wire/)
- [wireshark **1**](https://jasminides.com/tags/wireshark/)
- [WSDL **1**](https://jasminides.com/tags/wsdl/)
- [WSL **1**](https://jasminides.com/tags/wsl/)
- [阿里云 **1**](https://jasminides.com/tags/%E9%98%BF%E9%87%8C%E4%BA%91/)
- [阿里云 OSS **1**](https://jasminides.com/tags/%E9%98%BF%E9%87%8C%E4%BA%91-oss/)
- [安全 **1**](https://jasminides.com/tags/%E5%AE%89%E5%85%A8/)
- [备份 **1**](https://jasminides.com/tags/%E5%A4%87%E4%BB%BD/)
- [本地化 **1**](https://jasminides.com/tags/%E6%9C%AC%E5%9C%B0%E5%8C%96/)
- [编码 **1**](https://jasminides.com/tags/%E7%BC%96%E7%A0%81/)
- [并发编程 **2**](https://jasminides.com/tags/%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B/)
- [策略模式 **1**](https://jasminides.com/tags/%E7%AD%96%E7%95%A5%E6%A8%A1%E5%BC%8F/)
- [错误处理 **1**](https://jasminides.com/tags/%E9%94%99%E8%AF%AF%E5%A4%84%E7%90%86/)
- [多路复用 **1**](https://jasminides.com/tags/%E5%A4%9A%E8%B7%AF%E5%A4%8D%E7%94%A8/)
- [多平台博客发布工具 **1**](https://jasminides.com/tags/%E5%A4%9A%E5%B9%B3%E5%8F%B0%E5%8D%9A%E5%AE%A2%E5%8F%91%E5%B8%83%E5%B7%A5%E5%85%B7/)
- [访问控制 **1**](https://jasminides.com/tags/%E8%AE%BF%E9%97%AE%E6%8E%A7%E5%88%B6/)
- [分布式链路追踪 **2**](https://jasminides.com/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E9%93%BE%E8%B7%AF%E8%BF%BD%E8%B8%AA/)
- [服务反射协议 **1**](https://jasminides.com/tags/%E6%9C%8D%E5%8A%A1%E5%8F%8D%E5%B0%84%E5%8D%8F%E8%AE%AE/)
- [负载均衡 **1**](https://jasminides.com/tags/%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1/)
- [工具 **1**](https://jasminides.com/tags/%E5%B7%A5%E5%85%B7/)
- [监控 **1**](https://jasminides.com/tags/%E7%9B%91%E6%8E%A7/)
- [健康检查 **3**](https://jasminides.com/tags/%E5%81%A5%E5%BA%B7%E6%A3%80%E6%9F%A5/)
- [健康探针 **1**](https://jasminides.com/tags/%E5%81%A5%E5%BA%B7%E6%8E%A2%E9%92%88/)
- [可视化 **1**](https://jasminides.com/tags/%E5%8F%AF%E8%A7%86%E5%8C%96/)
- [拦截器 **1**](https://jasminides.com/tags/%E6%8B%A6%E6%88%AA%E5%99%A8/)
- [浏览器 **1**](https://jasminides.com/tags/%E6%B5%8F%E8%A7%88%E5%99%A8/)
- [模糊测试 **1**](https://jasminides.com/tags/%E6%A8%A1%E7%B3%8A%E6%B5%8B%E8%AF%95/)
- [内存 **1**](https://jasminides.com/tags/%E5%86%85%E5%AD%98/)
- [人工智能 **2**](https://jasminides.com/tags/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD/)
- [认证 **1**](https://jasminides.com/tags/%E8%AE%A4%E8%AF%81/)
- [容器 **2**](https://jasminides.com/tags/%E5%AE%B9%E5%99%A8/)
- [设计模式 **1**](https://jasminides.com/tags/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/)
- [时间处理 **1**](https://jasminides.com/tags/%E6%97%B6%E9%97%B4%E5%A4%84%E7%90%86/)
- [数据分析 **1**](https://jasminides.com/tags/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/)
- [通信模式 **1**](https://jasminides.com/tags/%E9%80%9A%E4%BF%A1%E6%A8%A1%E5%BC%8F/)
- [图片 **1**](https://jasminides.com/tags/%E5%9B%BE%E7%89%87/)
- [网络 **1**](https://jasminides.com/tags/%E7%BD%91%E7%BB%9C/)
- [网页探测 **1**](https://jasminides.com/tags/%E7%BD%91%E9%A1%B5%E6%8E%A2%E6%B5%8B/)
- [小米音箱 **1**](https://jasminides.com/tags/%E5%B0%8F%E7%B1%B3%E9%9F%B3%E7%AE%B1/)
- [小问题 **1**](https://jasminides.com/tags/%E5%B0%8F%E9%97%AE%E9%A2%98/)
- [协程 **1**](https://jasminides.com/tags/%E5%8D%8F%E7%A8%8B/)
- [循环 **1**](https://jasminides.com/tags/%E5%BE%AA%E7%8E%AF/)
- [邮件 **1**](https://jasminides.com/tags/%E9%82%AE%E4%BB%B6/)
- [域名 **1**](https://jasminides.com/tags/%E5%9F%9F%E5%90%8D/)
- [元数据 **1**](https://jasminides.com/tags/%E5%85%83%E6%95%B0%E6%8D%AE/)
- [证书 **1**](https://jasminides.com/tags/%E8%AF%81%E4%B9%A6/)
- [中间件 **1**](https://jasminides.com/tags/%E4%B8%AD%E9%97%B4%E4%BB%B6/)
- [抓包 **1**](https://jasminides.com/tags/%E6%8A%93%E5%8C%85/)
- [状态码 **1**](https://jasminides.com/tags/%E7%8A%B6%E6%80%81%E7%A0%81/)

 [Go to Top (Alt + G)](https://jasminides.com/tags/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801865033&bpp=3&bdt=138&idt=83&shv=r20250319&mjsv=m202503190101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=890696200465&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C42532524%2C31091178&oid=2&pvsid=1142246560934184&tmod=247288249&uas=0&nvt=1&fsapi=1&fc=1920&brdim=170%2C170%2C170%2C170%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=105)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## AI Integration and Art
前言 前段时间看到了一个项目 mi-gpt ,可以将你的小爱音箱接入 gpt，改造成专属于你的语音助手。
接下来就由作者来介绍小爱同学从零接入 deepseek 的过程。
设置环境变量和配置文件 mi-gpt 有两种部署方式，一是使用 docker 部署，二是使用 Node.js 进行部署，本文使用 docker 进行部署使用。
需要提供两个文件 .env 和 .migpt.js 文件，.migpt.js 是配置文件，包括一些配置，.env 是环境变量文件，存放 gpt 密钥相关文件。文件的例子可以从仓库里复制，然后进行相应的修改。
启动 使用以下命令启动 docker:
docker run -d --env-file $(pwd)/.env -v $(pwd)/.migpt.js:/app/.migpt.js idootop/mi-gpt:latest windows 环境下需要将$(pwd) 替换为绝对路径。
启动后可以通过 callAIKeywords 设置的关键字调用 ai 来响应用户的消息。
小结 本文介绍了使用 mi-gpt 升级你的闲置的小爱音箱，通过简单的测试和使用，个人感觉还不够完善，稳定性不够好，感兴趣的读者可以根据本文的内容进行自行搭建尝试。
参考 https://github.com/idootop/mi-gpt

 [post link to 使用 gpt 改造你的小米音箱](https://jasminides.com/posts/mi_gpt/)

前言 最近我发现各个群里出现了一股利用 AI 进行绘画的潮流，今天我也尝试使用 Stable Diffusion 模型 进行 AI 绘画。
Stable Diffusion 简介 Stable Diffusion 是一个文本到图像的模型，将使人们可以在几秒钟内创造出令人惊叹的艺术作品。它在速度和质量方面都有突破，这意味着它可以在消费级 GPU 上运行
开始 我们采用别人封装的 stable-diffusion-webui 平台进行绘画，由于各种条件限制，我们使用 github 上提供的 Google colab notbook 进行部署 (https://colab.research.google.com/drive/1IplUv47g9CgtlJmFnyT2sDyNYDEeMJDi?usp=sharing).
打开链接，我简单的看了下代码，前面是基础的安装运行环境、需要的 Python package .我们依次运行即可。
我们直接来到 1.4 Connect to Google Drive， 勾选 download\_if\_missing，然后到 https://huggingface.co/settings/tokens 复制你的 toekn 并填入。(huggingface 注册耗费了许多时间，reCAPTCHA 没有通过).
点击运行后就开始拉取模型。
如果运行发现报错了：
remote: Access to model CompVis/stable-diffusion-v-1-4-original is restricted and you are not in the authorized list. Visit https://huggingface.co/CompVis/stable-diffusion-v-1-4-original to ask for access. fatal: unable to access 'https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/': The requested URL returned error: 403 你需要到 https://huggingface.co/CompVis/stable-diffusion-v-1-4-original 授权模型的访问权限。授权后重新运行即可。
...

 [post link to AI 绘画初体验](https://jasminides.com/posts/ai%E7%BB%98%E7%94%BB%E5%88%9D%E4%BD%93%E9%AA%8C/) [Go to Top (Alt + G)](https://jasminides.com/tags/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2F%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801865410&bpp=3&bdt=396&idt=158&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=8360883050414&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95331833%2C95352052%2C95353420%2C95355301&oid=2&pvsid=1534197211427192&tmod=506265180&uas=0&nvt=1&fsapi=1&fc=1920&brdim=620%2C620%2C620%2C620%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=200)

[iframe](https://ep2.adtrafficquality.google/sodar/sodar2/232/runner.html)[iframe](https://www.google.com/recaptcha/api2/aframe)[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Xiao Ai Assistant Upgrade
目录

- [前言](https://jasminides.com/posts/mi_gpt/#%e5%89%8d%e8%a8%80)
- [设置环境变量和配置文件](https://jasminides.com/posts/mi_gpt/#%e8%ae%be%e7%bd%ae%e7%8e%af%e5%a2%83%e5%8f%98%e9%87%8f%e5%92%8c%e9%85%8d%e7%bd%ae%e6%96%87%e4%bb%b6)
- [启动](https://jasminides.com/posts/mi_gpt/#%e5%90%af%e5%8a%a8)
- [小结](https://jasminides.com/posts/mi_gpt/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/mi_gpt/#%e5%8f%82%e8%80%83)

## 前言

前段时间看到了一个项目 `mi-gpt` ,可以将你的小爱音箱接入 gpt，改造成专属于你的语音助手。

接下来就由作者来介绍小爱同学从零接入 deepseek 的过程。

## 设置环境变量和配置文件

mi-gpt 有两种部署方式，一是使用 docker 部署，二是使用 Node.js 进行部署，本文使用 docker 进行部署使用。

需要提供两个文件 .env 和 .migpt.js 文件，.migpt.js 是配置文件，包括一些配置，.env 是环境变量文件，存放 gpt 密钥相关文件。文件的例子可以从仓库里复制，然后进行相应的修改。

## 启动

使用以下命令启动 docker:

```
docker run -d --env-file $(pwd)/.env -v $(pwd)/.migpt.js:/app/.migpt.js idootop/mi-gpt:latest
复制
```

windows 环境下需要将$(pwd) 替换为绝对路径。

启动后可以通过 callAIKeywords 设置的关键字调用 ai 来响应用户的消息。

![alt text](https://jasminides.com/img/mi-gpt/image.png)

## 小结

本文介绍了使用 mi-gpt 升级你的闲置的小爱音箱，通过简单的测试和使用，个人感觉还不够完善，稳定性不够好，感兴趣的读者可以根据本文的内容进行自行搭建尝试。

## 参考

- [https://github.com/idootop/mi-gpt](https://github.com/idootop/mi-gpt)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fmi_gpt%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/mi_gpt/#top "Go to Top (Alt + G)")

## Upgrade Xiaomi Speaker
前言 前段时间看到了一个项目 mi-gpt ,可以将你的小爱音箱接入 gpt，改造成专属于你的语音助手。
接下来就由作者来介绍小爱同学从零接入 deepseek 的过程。
设置环境变量和配置文件 mi-gpt 有两种部署方式，一是使用 docker 部署，二是使用 Node.js 进行部署，本文使用 docker 进行部署使用。
需要提供两个文件 .env 和 .migpt.js 文件，.migpt.js 是配置文件，包括一些配置，.env 是环境变量文件，存放 gpt 密钥相关文件。文件的例子可以从仓库里复制，然后进行相应的修改。
启动 使用以下命令启动 docker:
docker run -d --env-file $(pwd)/.env -v $(pwd)/.migpt.js:/app/.migpt.js idootop/mi-gpt:latest windows 环境下需要将$(pwd) 替换为绝对路径。
启动后可以通过 callAIKeywords 设置的关键字调用 ai 来响应用户的消息。
小结 本文介绍了使用 mi-gpt 升级你的闲置的小爱音箱，通过简单的测试和使用，个人感觉还不够完善，稳定性不够好，感兴趣的读者可以根据本文的内容进行自行搭建尝试。
参考 https://github.com/idootop/mi-gpt

 [post link to 使用 gpt 改造你的小米音箱](https://jasminides.com/posts/mi_gpt/) [Go to Top (Alt + G)](https://jasminides.com/tags/%E5%B0%8F%E7%B1%B3%E9%9F%B3%E7%AE%B1/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2F%25E5%25B0%258F%25E7%25B1%25B3%25E9%259F%25B3%25E7%25AE%25B1%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801865037&bpp=3&bdt=213&idt=76&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=750211913766&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340&oid=2&pvsid=622208220354470&tmod=867320737&uas=0&nvt=1&fsapi=1&fc=1920&brdim=160%2C160%2C160%2C160%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=102)

[iframe](https://ep2.adtrafficquality.google/sodar/sodar2/232/runner.html)[iframe](https://www.google.com/recaptcha/api2/aframe)[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Node.js Build Solutions
前言 今天在编译构建一个 node.js 项目时，在构建过程中遇到了一些问题，本文将记录问题及对应的解决方案。
问题 1 在执行 npm run build 遇到此提示：
error Expected linebreaks to be 'LF' but found 'CRLF' linebreak-style 根据信息可以看出是 eslint 的报错，查看 .eslintrc.js 文件，修改 linebreak-style 对应的行：
'linebreak-style': \['error', process.platform === 'win32' ? 'windows' : 'unix'\], 重新运行命令，顺利构建成功。
这个问题的原因是项目的作者可能是使用 Linux 或 Mac 构建的，没有考虑 Windows 的情况，通过这行配置，可以根据运行的环境来决定 lint 规则。
问题 2 在执行 npm start 遇到了第二个问题：
Generating browser application bundles (phase: building)...node:internal/crypto/hash:79 this\[kHandle\] = new \_Hash(algorithm, xofLen, algorithmId, getHashCache()); ^ Error: error:0308010C:digital envelope routines::unsupported at new Hash (node:internal/crypto/hash:79:19) at Object.createHash (node:crypto:139:10) at BulkUpdateDecorator.hashFactory (D:\\code\\xx\\node\_modules\\webpack\\lib\\util\\createHash.js:145:18) at BulkUpdateDecorator.update (D:\\code\\xx\\node\_modules\\webpack\\lib\\util\\createHash.js:46:50) at RawSource.updateHash (D:\\code\\xx\\node\_modules\\webpack\\node\_modules\\webpack-sources\\lib\\RawSource.js:77:8) at NormalModule.\_initBuildHash (D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:880:17) at handleParseResult (D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:946:10) at D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:1040:4 at processResult (D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:755:11) at D:\\code\\xx\\node\_modules\\webpack\\lib\\NormalModule.js:819:5 { opensslErrorStack: \[ 'error:03000086:digital envelope routines::initialization error', 'error:0308010C:digital envelope routines::unsupported' \], library: 'digital envelope routines', reason: 'unsupported', code: 'ERR\_OSSL\_EVP\_UNSUPPORTED' } 根据这个报错，推测可能是啥 hash 算法不支持，通过查阅相关资料，得到以下解决方案：
...

 [post link to node.js 项目构建问题及解决](https://jasminides.com/posts/node_build_error/)

最近遇到前后端传输数据需要进行加密的需求，本篇文章就分别介绍使用 Node.js 和 go 进行 AES 加密解密的方法，AES 有很多不同的算法，如 aes192，aes-128-ecb，aes-256-cbc 等，根据不同的密钥长度会使用不同的算法。加密后的结果有两种表示方法：hex 和 base64，我们这里使用 hex.
golang 使用 golang 实现 aes 加密，我使用标准库的方法实现，我使用的 CBC 模式。
加密 func AesEncrypt(encryptStr string, key \[\]byte, iv string) (string, error) { encryptBytes := \[\]byte(encryptStr) block, err := aes.NewCipher(key) if err != nil { return "", err } blockSize := block.BlockSize() encryptBytes = pkcs5Padding(encryptBytes, blockSize) blockMode := cipher.NewCBCEncrypter(block, \[\]byte(iv)) encrypted := make(\[\]byte, len(encryptBytes)) blockMode.CryptBlocks(encrypted, encryptBytes) return hex.EncodeToString(encrypted), nil } 解密 func AesDecrypt(decryptStr string, key \[\]byte, iv string) (string, error) { decryptBytes, err := hex.DecodeString(decryptStr) if err != nil { return "", err } block, err := aes.NewCipher(key) if err != nil { return "", err } blockMode := cipher.NewCBCDecrypter(block, \[\]byte(iv)) decrypted := make(\[\]byte, len(decryptBytes)) blockMode.CryptBlocks(decrypted, decryptBytes) decrypted = pkcs5UnPadding(decrypted) return string(decrypted), nil } 运行加密解密例子 package main import ( "bytes" "crypto/aes" "crypto/cipher" "encoding/hex" "fmt" ) func AesEncrypt(encryptStr string, key \[\]byte, iv string) (string, error) { encryptBytes := \[\]byte(encryptStr) block, err := aes.NewCipher(key) if err != nil { return "", err } blockSize := block.BlockSize() encryptBytes = pkcs5Padding(encryptBytes, blockSize) blockMode := cipher.NewCBCEncrypter(block, \[\]byte(iv)) encrypted := make(\[\]byte, len(encryptBytes)) blockMode.CryptBlocks(encrypted, encryptBytes) return hex.EncodeToString(encrypted), nil } func AesDecrypt(decryptStr string, key \[\]byte, iv string) (string, error) { decryptBytes, err := hex.DecodeString(decryptStr) if err != nil { return "", err } block, err := aes.NewCipher(key) if err != nil { return "", err } blockMode := cipher.NewCBCDecrypter(block, \[\]byte(iv)) decrypted := make(\[\]byte, len(decryptBytes)) blockMode.CryptBlocks(decrypted, decryptBytes) decrypted = pkcs5UnPadding(decrypted) return string(decrypted), nil } func pkcs5Padding(cipherText \[\]byte, blockSize int) \[\]byte { padding := blockSize - len(cipherText)%blockSize padText := bytes.Repeat(\[\]byte{byte(padding)}, padding) return append(cipherText, padText...) } func pkcs5UnPadding(decrypted \[\]byte) \[\]byte { length := len(decrypted) unPadding := int(decrypted\[length-1\]) return decrypted\[:(length - unPadding)\] } func main() { data := "i am test data" key := \[\]byte("1111111111111111") iv := "1111122211111111" encrypt, err := AesEncrypt(data, key, iv) if err != nil { panic(err) return } fmt.Println(encrypt) decrypt, err := AesDecrypt(encrypt, key, iv) if err != nil { panic(err) } fmt.Println(decrypt) } ...

 [post link to 前后端使用 AES 加密传输数据](https://jasminides.com/posts/%E5%89%8D%E5%90%8E%E7%AB%AF%E4%BD%BF%E7%94%A8aes%E5%8A%A0%E5%AF%86%E4%BC%A0%E8%BE%93%E6%95%B0%E6%8D%AE/) [Go to Top (Alt + G)](https://jasminides.com/tags/node.js/#top "Go to Top (Alt + G)")

## Node.js Build Errors
目录

- [前言](https://jasminides.com/posts/node_build_error/#%e5%89%8d%e8%a8%80)
- [问题 1](https://jasminides.com/posts/node_build_error/#%e9%97%ae%e9%a2%98-1)
- [问题 2](https://jasminides.com/posts/node_build_error/#%e9%97%ae%e9%a2%98-2)
- [参考](https://jasminides.com/posts/node_build_error/#%e5%8f%82%e8%80%83)

## 前言

今天在编译构建一个 node.js 项目时，在构建过程中遇到了一些问题，本文将记录问题及对应的解决方案。

## 问题 1

在执行 `npm run build` 遇到此提示：

```
error  Expected linebreaks to be 'LF' but found 'CRLF'  linebreak-style
复制
```

根据信息可以看出是 eslint 的报错，查看 .eslintrc.js 文件，修改 linebreak-style 对应的行：

```
'linebreak-style': ['error', process.platform === 'win32' ? 'windows' : 'unix'],
复制
```

重新运行命令，顺利构建成功。

这个问题的原因是项目的作者可能是使用 Linux 或 Mac 构建的，没有考虑 Windows 的情况，通过这行配置，可以根据运行的环境来决定 lint 规则。

## 问题 2

在执行 `npm start` 遇到了第二个问题：

```
Generating browser application bundles (phase: building)...node:internal/crypto/hash:79
  this[kHandle] = new _Hash(algorithm, xofLen, algorithmId, getHashCache());
                  ^

Error: error:0308010C:digital envelope routines::unsupported
    at new Hash (node:internal/crypto/hash:79:19)
    at Object.createHash (node:crypto:139:10)
    at BulkUpdateDecorator.hashFactory (D:\code\xx\node_modules\webpack\lib\util\createHash.js:145:18)
    at BulkUpdateDecorator.update (D:\code\xx\node_modules\webpack\lib\util\createHash.js:46:50)
    at RawSource.updateHash (D:\code\xx\node_modules\webpack\node_modules\webpack-sources\lib\RawSource.js:77:8)
    at NormalModule._initBuildHash (D:\code\xx\node_modules\webpack\lib\NormalModule.js:880:17)
    at handleParseResult (D:\code\xx\node_modules\webpack\lib\NormalModule.js:946:10)
    at D:\code\xx\node_modules\webpack\lib\NormalModule.js:1040:4
    at processResult (D:\code\xx\node_modules\webpack\lib\NormalModule.js:755:11)
    at D:\code\xx\node_modules\webpack\lib\NormalModule.js:819:5 {
  opensslErrorStack: [\
    'error:03000086:digital envelope routines::initialization error',\
    'error:0308010C:digital envelope routines::unsupported'\
  ],
  library: 'digital envelope routines',
  reason: 'unsupported',
  code: 'ERR_OSSL_EVP_UNSUPPORTED'
}
复制
```

根据这个报错，推测可能是啥 hash 算法不支持，通过查阅相关资料，得到以下解决方案：

1 降级 Node.js 版本，降级版本至 V16 版本以使用不安全的 libssl 版本。显然这不是特别好的方法。

2 通过环境变量，让程序使用旧的 OpenSSL 提供程序

```shell
export NODE_OPTIONS=--openssl-legacy-provider

```

复制

Windows

```
set NODE_OPTIONS=--openssl-legacy-provider
复制
```

3 升级依赖

最佳作法是通过升级所使用的依赖。

## 参考

- [https://stackoverflow.com/questions/37826449/expected-linebreaks-to-be-lf-but-found-crlf-linebreak-style](https://stackoverflow.com/questions/37826449/expected-linebreaks-to-be-lf-but-found-crlf-linebreak-style)

- [https://stackoverflow.com/questions/69692842/error-message-error0308010cdigital-envelope-routinesunsupported](https://stackoverflow.com/questions/69692842/error-message-error0308010cdigital-envelope-routinesunsupported)


giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fnode_build_error%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/node_build_error/#top "Go to Top (Alt + G)")

## Go CSV Parsing Issues
问题 最近在使用 go 解析 csv 文件时，读取并打印 csv 的每行内容时，读取到第 11 行时，程序报错，提示：
record on line 11: wrong number of fields 分析 遇到这个问题，我第一反应是 csv 文件的格式有问题，于是我使用 cat 命令查看 csv 文件，发现 csv 文件的格式是正确的，没有问题。 并查看分隔符是正确的，于是可以得出 csv 文件是没有问题的。
接下来就查看所使用的标准库 encoding/csv，通过查阅文档及 issue, 发现 csv 包中的 FieldsPerRecord 字段，FieldsPerRecord 表示 csv 文件每行的预期字段数， 如果为正数，则读取的每条记录都必须有对应的字段数，如果为 0，则会以第一条记录的数量为标准，接下来每行都必须有对应的字段数，如果为负数，则不会检查字段数。
修改后的代码如下：
package main import ( "encoding/csv" "fmt" "io" "log" "os" ) func main() { file, err := os.Open("./xx.csv") if err != nil { log.Fatal(err) } defer file.Close() // 创建一个 CSV reader reader := csv.NewReader(file) reader.FieldsPerRecord = -1 // 循环读取 CSV 文件中的每一行数据 for { record, err := reader.Read() if err == io.EOF { break } if err != nil { log.Fatal(err) } // 处理每一行数据 fmt.Println(record) fmt.Println(len(record)) } } 小结 本文记录了在使用 go 解析 csv 时遇到字段数不匹配的问题，并分析了问题的原因，并给出了相应的解决方法。
...

 [post link to go 解析 csv 文件报错](https://jasminides.com/posts/read_csv_error/) [Go to Top (Alt + G)](https://jasminides.com/tags/csv/#top "Go to Top (Alt + G)")

## Go Programming Resources
问题 最近在使用 go 解析 csv 文件时，读取并打印 csv 的每行内容时，读取到第 11 行时，程序报错，提示：
record on line 11: wrong number of fields 分析 遇到这个问题，我第一反应是 csv 文件的格式有问题，于是我使用 cat 命令查看 csv 文件，发现 csv 文件的格式是正确的，没有问题。 并查看分隔符是正确的，于是可以得出 csv 文件是没有问题的。
接下来就查看所使用的标准库 encoding/csv，通过查阅文档及 issue, 发现 csv 包中的 FieldsPerRecord 字段，FieldsPerRecord 表示 csv 文件每行的预期字段数， 如果为正数，则读取的每条记录都必须有对应的字段数，如果为 0，则会以第一条记录的数量为标准，接下来每行都必须有对应的字段数，如果为负数，则不会检查字段数。
修改后的代码如下：
package main import ( "encoding/csv" "fmt" "io" "log" "os" ) func main() { file, err := os.Open("./xx.csv") if err != nil { log.Fatal(err) } defer file.Close() // 创建一个 CSV reader reader := csv.NewReader(file) reader.FieldsPerRecord = -1 // 循环读取 CSV 文件中的每一行数据 for { record, err := reader.Read() if err == io.EOF { break } if err != nil { log.Fatal(err) } // 处理每一行数据 fmt.Println(record) fmt.Println(len(record)) } } 小结 本文记录了在使用 go 解析 csv 时遇到字段数不匹配的问题，并分析了问题的原因，并给出了相应的解决方法。
...

 [post link to go 解析 csv 文件报错](https://jasminides.com/posts/read_csv_error/)

前言 电子邮件是现代办公和通信中不可或缺的工具，它广泛应用于数据交换和工作沟通。为了更高效地处理邮件内容，我们可以借助程序来实现自动化处理。本文将详细介绍如何使用 Go 语言来接收和处理电子邮件。
通过查阅资料，了解到可以通过 IMAP 协议来接收电子邮件，IMAP 协议是电子邮件接收协议，它允许客户端通过网络连接到邮件服务器，并从服务器上下载邮件。除了 IMAP 协议，还有 POP3 协议，POP3 协议与 IMAP 协议类似，但它在在客户端上对邮件的操作不会反馈到邮件服务器上，也就是说，在客户端的操作不会影响服务器上的邮件。当你需要从多个邮件客户端访问邮件时，IMAP 协议是一个更好的选择。
go-imap 通过对比不同的库，最后选择了 go-imap 库，它是一个基于 IMAP 协议的 Go 语言库，可以通过它构建客户端或者服务端。
安装 可以通过以下命令安装：
go get github.com/emersion/go-imap 使用 我们将通过官方的例子进行切入：
先通过 DialTLS 连接对应的电子邮箱 IMAP 服务器，然后通过登录邮箱，获取所有的邮箱文件夹，最后选择收件箱，获取收件箱中最新的 4 封邮件，并打印没封邮件的主题。
运行代码：
2024/11/23 16:16:11 Connecting to server... 2024/11/23 16:16:11 Connected 2024/11/23 16:16:12 Logged in 2024/11/23 16:16:12 Mailboxes: 2024/11/23 16:16:13 \* 其他文件夹 2024/11/23 16:16:13 \* Drafts 2024/11/23 16:16:13 \* Deleted Messages 2024/11/23 16:16:13 \* Sent Messages 2024/11/23 16:16:13 \* Junk 2024/11/23 16:16:13 \* INBOX 2024/11/23 16:16:13 Flags for INBOX: \[\\Answered \\Flagged \\Deleted \\Draft \\Seen\] 2024/11/23 16:16:13 Last 4 messages: 2024/11/23 16:16:13 \* =?GBK?B?xx?= 2024/11/23 16:16:13 \* =?GBK?B?xxx?= 2024/11/23 16:16:13 \* =?GBK?B?xx==?= 2024/11/23 16:16:13 \* =?GBK?B?xx+k=?= 2024/11/23 16:16:13 Done! 可以看到打印出来的邮件主题是乱码，通过查询资料，了解到邮件的字段是采用特殊编码的，需要进行解码。可以通过 https://github.com/emersion/go-message 这个库进行解码。
...

 [post link to Go Recivie Email](https://jasminides.com/posts/go-recivie-email/)

前言 最近需要调用一个第三方的接口进行数据的采集，这个接口是基于 SOAP 协议的，所以需要使用 soap 相关的客户端进行调用。于是我调研了一些开源的 golang 的 soap 客户端，发现 go-soap 这个库的文档比较完善，而且使用起来也比较简单，所以就选择了这个库。
安装 使用以下命令进行安装：
go get github.com/tiaguinho/gosoap 使用 由于目前没有特别好的例子，这里就以官方的例子进行说明。
官方的代码如下：
package main import ( "encoding/xml" "log" "net/http" "time" "github.com/tiaguinho/gosoap" ) // GetIPLocationResponse will hold the Soap response type GetIPLocationResponse struct { GetIPLocationResult string \`xml:"GetIpLocationResult"\` } // GetIPLocationResult will type GetIPLocationResult struct { XMLName xml.Name \`xml:"GeoIP"\` Country string \`xml:"Country"\` State string \`xml:"State"\` } var ( r GetIPLocationResponse ) func main() { httpClient := &http.Client{ Timeout: 1500 \* time.Millisecond, } soap, err := gosoap.SoapClient("http://wsgeoip.lavasoft.com/ipservice.asmx?WSDL", httpClient) if err != nil { log.Fatalf("SoapClient error: %s", err) } // Use gosoap.ArrayParams to support fixed position params params := gosoap.Params{ "sIp": "8.8.8.8", } res, err := soap.Call("GetIpLocation", params) if err != nil { log.Fatalf("Call error: %s", err) } res.Unmarshal(&r) // GetIpLocationResult will be a string. We need to parse it to XML result := GetIPLocationResult{} err = xml.Unmarshal(\[\]byte(r.GetIPLocationResult), &result) if err != nil { log.Fatalf("xml.Unmarshal error: %s", err) } if result.Country != "US" { log.Fatalf("error: %+v", r) } log.Println("Country: ", result.Country) log.Println("State: ", result.State) } 可以看到 go-soap 的使用跟常规的 http client 的使用方法类似，都是创建一个连接，准备方法的参数，然后调用相应的方法。 这段代码展示了如何使用 go-soap 库连接 SOAP 服务、发送请求、处理响应，以及如何解析 XML 格式的返回数据。
...

 [post link to go-soap 简介](https://jasminides.com/posts/go-soap-desc/)

前言 今天在 Github 查看一些开源项目时，发现了一个"人性化"的项目 go-humanize，此项目可以将一些常见的容量、时间、千分位转换为人们可以理解的形式，例如一个文件大小是 2000000 bytes，我们不能很好的理解，但如果告诉你是 2mb，我们就能很好的理解了。go-humanize 就是方便的将一些不太能快速理解的数字转换为人们可以理解的形式。
安装 使用以下命令安装：
go get github.com/dustin/go-humanize 使用 接下来分别介绍一些常见的功能。
容量转换 现在我们有一个文件大小是 52854982 bytes，我们使用 humanize 包的 Bytes 方法将其转换为人们可以理解的形式 53MB，也可以使用 IBytes 方法转换为 MIB 单位的值。也可以使用 ParseBytes 方法将可以理解的形式转换为 bytes 单位的值。
fmt.Printf("That file is %s.\\n", humanize.IBytes(52854982)) fmt.Printf("That file is %s.", humanize.Bytes(52854982)) 时间转换 时间转换与容量转换类型，使用方法十分类似，使用方法如下：
t := time.Now().Add(time.Hour \* -7) fmt.Printf("This was touched %s.", humanize.Time(t)) //This was touched 7 hours ago. Time 根据相对时间转换为人们可以理解的形式，例如：xx 天之前、xx 小时之后等形式。
千分位转换 如果我们想在数字中添加逗号，就可以使用 Comma 方法，例如在处理金额时，我们通常会使用逗号将数字分隔开，例如 1,000,000,000
fmt.Printf("num is %s.", humanize.Comma(1000000000)) 还可以使用 Commaf 方法将浮点数转换为千分位形式。
位序 在日常使用中，我们有时需要表示位序例如 1st、2nd、3rd、4th 等，humanize 包也提供了相应的功能。
...

 [post link to go humanize 介绍](https://jasminides.com/posts/go-humanize-introduce-/)

katana 介绍 katana 是一款强大的新一代的网络爬虫工具，通过使用 katana，用户能够快速的进行互联网资源的爬取和渗透测试阶段的收集任务。
特点 katana 有以下特点：
快速及高可配置的网络爬虫 标准及无头模式 主动和被动模式 JavaScript 脚本爬取解析 定制的表单内容自动填充 爬取范围控制 可自定义设置输出字段 输入数据 支持标准输入 (STDIN)，URL 和列表 (LIST) 输出数据 支持 STDOUT、文件和 JSON 格式 安装 接下来介绍如何安装 katana
katana 的安装需要 go1.18 版本以上，可以执行以下命令或下载 Github 仓库的发布版本。
go install github.com/projectdiscovery/katana/cmd/katana@latest windows 在安装中可能会遇到以下报错：
github.com/smacker/go-tree-sitter/javascript: build constraints exclude all Go files in C:\\Users\\overstarry\\go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\javascript # github.com/smacker/go-tree-sitter go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:17:18: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:21:21: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:25:20: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:30:26: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:34:20: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:38:32: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:43:9: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:46:18: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:68:40: undefined: Node 可以使用以下命令解决：
...

 [post link to katana 新一代的爬虫工具](https://jasminides.com/posts/katana/)

slug 介绍 slug 在不同的场景有不同的意义，在 URL 中表示一种用于描述资源的短简洁易于理解的资源描述符，在数据库系统中还可以用于描述资源的唯一标识符，总的来说 slug 可以用来标识和描述资源的文本标识符，有很好的可读性和唯一性。
本文将介绍 golang 中如何根据字符串生成相应的 slug 文本。
安装 执行 go get -u github.com/gosimple/slug 来安装 slug
使用 先介绍 slug 库的基础使用方法：
package main import ( "fmt" "github.com/gosimple/slug" ) func main() { text := slug.Make("overstarry home") fmt.Println(text) text = slug.Make("text generate") fmt.Println(text) } 运行后：
overstarry-home text-generate 除了基础的转换功能，slug 还支持将不同的语言进行转换，查看下面的例子：
func main() { text := slug.Make("overstarry home") fmt.Println(text) text = slug.Make("text generate") fmt.Println(text) text = slug.Make("Hellö Wörld хелло ворлд") fmt.Println(text) someText := slug.Make("影師") fmt.Println(someText) enText := slug.MakeLang("This & that", "en") fmt.Println(enText) } overstarry-home text-generate hello-world-khello-vorld ping-guo this-and-that 如果想要保留大写字母，可以设置 slug.Lowercase 参数来实现。如果想实现自定义的替换可以使用 slug.CustomSub 来实现。
...

 [post link to golang 生成 slug 字符串](https://jasminides.com/posts/go_generate_slug/)

Google Analytics 介绍 Google Analytics（分析）4 是一项分析服务，用于衡量您的网站和应用中的流量和互动情况。本文将介绍如何通过调用 Google Analytics admin API 来生成 Google Analytics 衡量 ID.
配置 启用 API 在 Google Cloud console 后台 API 和服务 启用 Google Analytics Admin API。
配置服务账号 为了调用 API，我们需要创建一个服务账号，然后为创建的服务账号添加密钥。
需要注意的是还需要在 Google Analytics 为服务账号添加权限，不然请求接口会没数据。
安装 go 客户端 接下来安装 go 客户端：
go get google.golang.org/api/analyticsadmin/v1alpha 生成流程 接下来我们会按照常规的 id 生成流程编写相应的代码，流程: 1 获取账号信息
通过 List 接口获取当前服务账号所拥有的所有 Google Analytics 账户信息。
accountsService := analyticsadmin.NewAccountsService(service) accountsReply, err := accountsService.List().Do(); if err != nil { log.Fatal("list account err",err) return } for \_,acc := range accountsReply.Accounts { fmt.Println(acc.Name) } 2 创建媒体资源
...

 [post link to Go 生成 Google analytics 衡量 ID](https://jasminides.com/posts/gogenerategaid/)

前言 本文介绍一个 go 汉字转拼音的库 go-pinyin，可以从名字看出这个库的功能就是将汉字转换为相应的拼音。接下来就由我来简单的介绍 go-pinyin。
安装 使用此命令安装：go get github.com/mozillazg/go-pinyin
cli 安装 如果你的 go 版本在 1.17 以下使用此命令安装：go get -u github.com/mozillazg/go-pinyin/cli/pinyin。1.17 及以上版本使用此命令安装：go install github.com/mozillazg/go-pinyin/cli/pinyin@latest。
使用 接下来将分别介绍 cli 的使用和 API 的使用。
cli 使用 安装完在终端输入 pinyin，可以看到使用的方法，尝试一个汉字，可以看到相应的拼音，但也可以看出对多音字的支持有问题。 $ pinyin 中国 zhōng guó $ pinyin 重庆 zhòng qìng 接下来介绍 API 的使用。
api 使用 通过查看文档，可以看出主要是 2 个方法 pinyin.NewArgs 和 pinyin.Pinyin 。
pinyin.NewArgs 创建包含默认配置的 Args, 可以通过修改 Args 的成员来使用不同的模式。
type Args struct { Style int // 拼音风格（默认：Normal) Heteronym bool // 是否启用多音字模式（默认：禁用） Separator string // Slug 中使用的分隔符（默认：-) // 处理没有拼音的字符（默认忽略没有拼音的字符） // 函数返回的 slice 的长度为 0 则表示忽略这个字符 Fallback func(r rune, a Args) \[\]string } pinyin.Pinyin 就是将汉字转为拼音。
...

 [post link to go 汉字转拼音 go-pinyin](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/)

前言 今天介绍一个 go 库 - mergo, mergo 用来方便的合并 struct 和 map ,可以将结构体的字段赋值到 map 中，可以将 map 的值赋值给结构体的字段。
Mergo 通过在零值字段中设置默认值来合并同类型的 struct 和 map。Mergo 不会合并未导出（私有）字段。它会递归合并任何已导出的字段。它也不会合并 map 中的结构体（因为它们无法使用 Go 反射寻址）。
Mergo 在很多知名项目中被使用，如 containerd、k8s、loki 等。
安装 使用以下命令安装 mergo : go get -u dario.cat/mergo
使用 接下来介绍 mergo 的基础使用和高级用法。
基础使用 mergo 提供了 2 个主要函数：Merge 和 Map, Mergo 用来合并 2 个相同结构的 struct 和 map, Map 用来在结构和 map 之间赋值。
例子：
package main import ( "fmt" "log" "github.com/imdario/mergo" ) type redisConfig struct { Address string Port int DB int UserName string PassWord string } var defaultConfig = redisConfig{ Address: "127.0.0.1", Port: 6379, DB: 1, UserName: "123", PassWord: "123", } func main() { var config redisConfig if err := mergo.Merge(&config, defaultConfig); err != nil { log.Fatal(err) } fmt.Println("redis address: ", config.Address) fmt.Println("redis port: ", config.Port) fmt.Println("redis db: ", config.DB) fmt.Println("redis username: ", config.UserName) fmt.Println("redis password: ", config.PassWord) var m = make(map\[string\]interface{}) if err := mergo.Map(&m, defaultConfig); err != nil { log.Fatal(err) } fmt.Println(m) } 接下来介绍一些高级用法：
...

 [post link to mergo 介绍](https://jasminides.com/posts/mergo_desc/)

前言 本文介绍 conc - 一个更好的 go 并发库，sourcegraph 在日常开发中使用 go 原生并发出现了问题，由此开发了 conc，相比标准并发代码更优雅，代码更少，下面展示一个例子，可以看出代码减少了许多。
type propagatedPanic struct { val any stack \[\]byte } func main() { done := make(chan \*propagatedPanic) go func() { defer func() { if v := recover(); v != nil { done <- &propagatedPanic{ val: v, stack: debug.Stack(), } } else { done <- nil } }() doSomethingThatMightPanic() }() if val := <-done; val != nil { panic(val) } } // conc func main() { var wg conc.WaitGroup wg.Go(doSomethingThatMightPanic) // panics with a nice stacktrace wg.Wait() } 安装 使用以下命令进行安装：go get github.com/sourcegraph/conc
...

 [post link to conc 一个更好的 go 并发库](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/) [Go to Top (Alt + G)](https://jasminides.com/tags/go/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201736&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fgo%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801870003&bpp=12&bdt=227&idt=255&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=167283578217&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95353386%2C95353929&oid=2&pvsid=3523505967232147&tmod=1088080758&uas=0&nvt=1&fsapi=1&fc=1920&brdim=20%2C20%2C20%2C20%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=273)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## CSV Parsing Error
目录

- [问题](https://jasminides.com/posts/read_csv_error/#%e9%97%ae%e9%a2%98)
- [分析](https://jasminides.com/posts/read_csv_error/#%e5%88%86%e6%9e%90)
- [小结](https://jasminides.com/posts/read_csv_error/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/read_csv_error/#%e5%8f%82%e8%80%83)

## 问题

最近在使用 go 解析 csv 文件时，读取并打印 csv 的每行内容时，读取到第 11 行时，程序报错，提示：

```console
record on line 11: wrong number of fields

```

复制

## 分析

遇到这个问题，我第一反应是 csv 文件的格式有问题，于是我使用 `cat` 命令查看 csv 文件，发现 csv 文件的格式是正确的，没有问题。
并查看分隔符是正确的，于是可以得出 csv 文件是没有问题的。

接下来就查看所使用的标准库 encoding/csv，通过查阅文档及 issue, 发现 csv 包中的 FieldsPerRecord 字段，FieldsPerRecord 表示 csv 文件每行的预期字段数，
如果为正数，则读取的每条记录都必须有对应的字段数，如果为 0，则会以第一条记录的数量为标准，接下来每行都必须有对应的字段数，如果为负数，则不会检查字段数。

修改后的代码如下：

```go
package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"os"
)

func main() {
	file, err := os.Open("./xx.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	// 创建一个 CSV reader
	reader := csv.NewReader(file)
	reader.FieldsPerRecord = -1
	// 循环读取 CSV 文件中的每一行数据
	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		// 处理每一行数据
		fmt.Println(record)
		fmt.Println(len(record))
	}
}

```

复制

## 小结

本文记录了在使用 go 解析 csv 时遇到字段数不匹配的问题，并分析了问题的原因，并给出了相应的解决方法。

## 参考

- [https://pkg.go.dev/encoding/csv#Reader.FieldsPerRecord](https://pkg.go.dev/encoding/csv#Reader.FieldsPerRecord)
- [https://stackoverflow.com/questions/61336787/how-do-i-fix-the-wrong-number-of-fields-with-the-missing-commas-in-csv-file-in](https://stackoverflow.com/questions/61336787/how-do-i-fix-the-wrong-number-of-fields-with-the-missing-commas-in-csv-file-in)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fread_csv_error%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/read_csv_error/#top "Go to Top (Alt + G)")

## Receive Emails with Go
目录

- [前言](https://jasminides.com/posts/go-recivie-email/#%e5%89%8d%e8%a8%80)
- [go-imap](https://jasminides.com/posts/go-recivie-email/#go-imap)
  - [安装](https://jasminides.com/posts/go-recivie-email/#%e5%ae%89%e8%a3%85)
  - [使用](https://jasminides.com/posts/go-recivie-email/#%e4%bd%bf%e7%94%a8)
- [参考](https://jasminides.com/posts/go-recivie-email/#%e5%8f%82%e8%80%83)

## 前言

电子邮件是现代办公和通信中不可或缺的工具，它广泛应用于数据交换和工作沟通。为了更高效地处理邮件内容，我们可以借助程序来实现自动化处理。本文将详细介绍如何使用 Go 语言来接收和处理电子邮件。

通过查阅资料，了解到可以通过 IMAP 协议来接收电子邮件，IMAP 协议是电子邮件接收协议，它允许客户端通过网络连接到邮件服务器，并从服务器上下载邮件。除了 IMAP 协议，还有 POP3 协议，POP3 协议与 IMAP 协议类似，但它在在客户端上对邮件的操作不会反馈到邮件服务器上，也就是说，在客户端的操作不会影响服务器上的邮件。当你需要从多个邮件客户端访问邮件时，IMAP 协议是一个更好的选择。

## go-imap

通过对比不同的库，最后选择了 go-imap 库，它是一个基于 IMAP 协议的 Go 语言库，可以通过它构建客户端或者服务端。

### 安装

可以通过以下命令安装：

```bash
go get github.com/emersion/go-imap

```

复制

### 使用

我们将通过官方的例子进行切入：

![alt text](https://jasminides.com/img/imap/carbon.png)

先通过 DialTLS 连接对应的电子邮箱 IMAP 服务器，然后通过登录邮箱，获取所有的邮箱文件夹，最后选择收件箱，获取收件箱中最新的 4 封邮件，并打印没封邮件的主题。

运行代码：

```console
2024/11/23 16:16:11 Connecting to server...
2024/11/23 16:16:11 Connected
2024/11/23 16:16:12 Logged in
2024/11/23 16:16:12 Mailboxes:
2024/11/23 16:16:13 * 其他文件夹
2024/11/23 16:16:13 * Drafts
2024/11/23 16:16:13 * Deleted Messages
2024/11/23 16:16:13 * Sent Messages
2024/11/23 16:16:13 * Junk
2024/11/23 16:16:13 * INBOX
2024/11/23 16:16:13 Flags for INBOX: [\Answered \Flagged \Deleted \Draft \Seen]
2024/11/23 16:16:13 Last 4 messages:
2024/11/23 16:16:13 * =?GBK?B?xx?=
2024/11/23 16:16:13 * =?GBK?B?xxx?=
2024/11/23 16:16:13 * =?GBK?B?xx==?=
2024/11/23 16:16:13 * =?GBK?B?xx+k=?=
2024/11/23 16:16:13 Done!

```

复制

可以看到打印出来的邮件主题是乱码，通过查询资料，了解到邮件的字段是采用特殊编码的，需要进行解码。可以通过 [https://github.com/emersion/go-message](https://github.com/emersion/go-message) 这个库进行解码。

修改后的代码如下：

![alt text](https://jasminides.com/img/imap/carbon%20%282%29.png)

通过设置 CharsetReader 顺利解码，主题顺利打印成功。

## 参考

- [https://www.cloudflare.com/learning/email-security/what-is-imap/](https://www.cloudflare.com/learning/email-security/what-is-imap/)
- [https://support.microsoft.com/en-us/office/what-are-imap-and-pop-ca2c5799-49f9-4079-aefe-ddca85d5b1c9](https://support.microsoft.com/en-us/office/what-are-imap-and-pop-ca2c5799-49f9-4079-aefe-ddca85d5b1c9)
- [https://github.com/emersion/go-imap/tree/v1](https://github.com/emersion/go-imap/tree/v1)
- [https://datatracker.ietf.org/doc/html/rfc3501](https://datatracker.ietf.org/doc/html/rfc3501)
- [https://github.com/emersion/go-message?tab=readme-ov-file](https://github.com/emersion/go-message?tab=readme-ov-file)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fgo-recivie-email%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/go-recivie-email/#top "Go to Top (Alt + G)")

## Go Programming Resources
前言 电子邮件是现代办公和通信中不可或缺的工具，它广泛应用于数据交换和工作沟通。为了更高效地处理邮件内容，我们可以借助程序来实现自动化处理。本文将详细介绍如何使用 Go 语言来接收和处理电子邮件。
通过查阅资料，了解到可以通过 IMAP 协议来接收电子邮件，IMAP 协议是电子邮件接收协议，它允许客户端通过网络连接到邮件服务器，并从服务器上下载邮件。除了 IMAP 协议，还有 POP3 协议，POP3 协议与 IMAP 协议类似，但它在在客户端上对邮件的操作不会反馈到邮件服务器上，也就是说，在客户端的操作不会影响服务器上的邮件。当你需要从多个邮件客户端访问邮件时，IMAP 协议是一个更好的选择。
go-imap 通过对比不同的库，最后选择了 go-imap 库，它是一个基于 IMAP 协议的 Go 语言库，可以通过它构建客户端或者服务端。
安装 可以通过以下命令安装：
go get github.com/emersion/go-imap 使用 我们将通过官方的例子进行切入：
先通过 DialTLS 连接对应的电子邮箱 IMAP 服务器，然后通过登录邮箱，获取所有的邮箱文件夹，最后选择收件箱，获取收件箱中最新的 4 封邮件，并打印没封邮件的主题。
运行代码：
2024/11/23 16:16:11 Connecting to server... 2024/11/23 16:16:11 Connected 2024/11/23 16:16:12 Logged in 2024/11/23 16:16:12 Mailboxes: 2024/11/23 16:16:13 \* 其他文件夹 2024/11/23 16:16:13 \* Drafts 2024/11/23 16:16:13 \* Deleted Messages 2024/11/23 16:16:13 \* Sent Messages 2024/11/23 16:16:13 \* Junk 2024/11/23 16:16:13 \* INBOX 2024/11/23 16:16:13 Flags for INBOX: \[\\Answered \\Flagged \\Deleted \\Draft \\Seen\] 2024/11/23 16:16:13 Last 4 messages: 2024/11/23 16:16:13 \* =?GBK?B?xx?= 2024/11/23 16:16:13 \* =?GBK?B?xxx?= 2024/11/23 16:16:13 \* =?GBK?B?xx==?= 2024/11/23 16:16:13 \* =?GBK?B?xx+k=?= 2024/11/23 16:16:13 Done! 可以看到打印出来的邮件主题是乱码，通过查询资料，了解到邮件的字段是采用特殊编码的，需要进行解码。可以通过 https://github.com/emersion/go-message 这个库进行解码。
...

 [post link to Go Recivie Email](https://jasminides.com/posts/go-recivie-email/)

前言 今天在 Github 查看一些开源项目时，发现了一个"人性化"的项目 go-humanize，此项目可以将一些常见的容量、时间、千分位转换为人们可以理解的形式，例如一个文件大小是 2000000 bytes，我们不能很好的理解，但如果告诉你是 2mb，我们就能很好的理解了。go-humanize 就是方便的将一些不太能快速理解的数字转换为人们可以理解的形式。
安装 使用以下命令安装：
go get github.com/dustin/go-humanize 使用 接下来分别介绍一些常见的功能。
容量转换 现在我们有一个文件大小是 52854982 bytes，我们使用 humanize 包的 Bytes 方法将其转换为人们可以理解的形式 53MB，也可以使用 IBytes 方法转换为 MIB 单位的值。也可以使用 ParseBytes 方法将可以理解的形式转换为 bytes 单位的值。
fmt.Printf("That file is %s.\\n", humanize.IBytes(52854982)) fmt.Printf("That file is %s.", humanize.Bytes(52854982)) 时间转换 时间转换与容量转换类型，使用方法十分类似，使用方法如下：
t := time.Now().Add(time.Hour \* -7) fmt.Printf("This was touched %s.", humanize.Time(t)) //This was touched 7 hours ago. Time 根据相对时间转换为人们可以理解的形式，例如：xx 天之前、xx 小时之后等形式。
千分位转换 如果我们想在数字中添加逗号，就可以使用 Comma 方法，例如在处理金额时，我们通常会使用逗号将数字分隔开，例如 1,000,000,000
fmt.Printf("num is %s.", humanize.Comma(1000000000)) 还可以使用 Commaf 方法将浮点数转换为千分位形式。
位序 在日常使用中，我们有时需要表示位序例如 1st、2nd、3rd、4th 等，humanize 包也提供了相应的功能。
...

 [post link to go humanize 介绍](https://jasminides.com/posts/go-humanize-introduce-/)

katana 介绍 katana 是一款强大的新一代的网络爬虫工具，通过使用 katana，用户能够快速的进行互联网资源的爬取和渗透测试阶段的收集任务。
特点 katana 有以下特点：
快速及高可配置的网络爬虫 标准及无头模式 主动和被动模式 JavaScript 脚本爬取解析 定制的表单内容自动填充 爬取范围控制 可自定义设置输出字段 输入数据 支持标准输入 (STDIN)，URL 和列表 (LIST) 输出数据 支持 STDOUT、文件和 JSON 格式 安装 接下来介绍如何安装 katana
katana 的安装需要 go1.18 版本以上，可以执行以下命令或下载 Github 仓库的发布版本。
go install github.com/projectdiscovery/katana/cmd/katana@latest windows 在安装中可能会遇到以下报错：
github.com/smacker/go-tree-sitter/javascript: build constraints exclude all Go files in C:\\Users\\overstarry\\go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\javascript # github.com/smacker/go-tree-sitter go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:17:18: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:21:21: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:25:20: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:30:26: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:34:20: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:38:32: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:43:9: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:46:18: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:68:40: undefined: Node 可以使用以下命令解决：
...

 [post link to katana 新一代的爬虫工具](https://jasminides.com/posts/katana/)

前言 cdn 刷新是 cdn 使用过程中的一项重要的功能，通过刷新功能，您可以删除 CDN 节点上已经缓存的资源，并强制 CDN 节点回源站获取最新资源，适用于源站资源更新和发布、违规资源清理、域名配置变更等。
接下来将分别讲述 阿里云 CDN、AWS cloudfront、Cloudflare cdn 使用 go 语言进行 cdn 的刷新操作的。
阿里云刷新 cdn 如何刷新 阿里云 cdn 的缓存呢？只需使用 阿里云 openapi 的 go sdk 即可，通过查阅文档，我们只需使用 RefreshObjectCaches API 即可刷新阿里云 cdn 的缓存，RefreshObjectCaches 有以下参数：
ObjectPath: 刷新的url ,多个 url 使用换行符进行分隔 ObjectType: 刷新任务的类型，有以下类型 File（默认值）：文件刷新。 Directory：目录刷新。 Regex：正则刷新。 IgnoreParams：去参数刷新。去参数指的是去除请求 URL 中?及?之后的参数，去参数刷新指的是用户先通过接口提交去参数后的 URL，然后用户提交的待刷新 URL 将会与已缓存资源的 URL 进行去参数匹配，如果已缓存资源的 URL 去参数以后与待刷新 URL 匹配，那么 CDN 节点将对缓存资源执行刷新处理。 Force: 当回源内容和源站资源对比后不一致时，是否刷新对应目录下的资源。默认为 false。 下面是一个例子：
package main import ( cdn20180510 "github.com/alibabacloud-go/cdn-20180510/v4/client" openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client" util "github.com/alibabacloud-go/tea-utils/v2/service" "github.com/alibabacloud-go/tea/tea" "os" ) func CreateClient(accessKeyId \*string, accessKeySecret \*string) (result \*cdn20180510.Client, err error) { config := &openapi.Config{ AccessKeyId: accessKeyId, AccessKeySecret: accessKeySecret, } config.Endpoint = tea.String("cdn.ap-southeast-1.aliyuncs.com") result = &cdn20180510.Client{} result, err = cdn20180510.NewClient(config) return result, err } func main() { client, err := CreateClient(tea.String(os.Getenv("ALIBABA\_CLOUD\_ACCESS\_KEY\_ID")), tea.String(os.Getenv("ALIBABA\_CLOUD\_ACCESS\_KEY\_SECRET"))) if err != nil { return } refreshObjectCachesRequest := &cdn20180510.RefreshObjectCachesRequest{ ObjectPath: tea.String("http://example.com/image/1.png\\\\\n\\t\\thttp://aliyundoc.com/image/2.png"), } runtime := &util.RuntimeOptions{} \_, err = client.RefreshObjectCachesWithOptions(refreshObjectCachesRequest, runtime) if err != nil { return } return } aws cloudfront 接下来讲解 aws cloudfront 如何刷新 cdn，cloudfront 刷新缓存的操作叫使文件失效，通过查阅 cloudfront 的 API 文档，发现可以使用 CreateInvalidation 来创建失效。可以使用 aws go sdk 来进行操作。
...

 [post link to Go 刷新 cdn](https://jasminides.com/posts/go_refresh_cdn/)

前言 本文介绍一个 go 汉字转拼音的库 go-pinyin，可以从名字看出这个库的功能就是将汉字转换为相应的拼音。接下来就由我来简单的介绍 go-pinyin。
安装 使用此命令安装：go get github.com/mozillazg/go-pinyin
cli 安装 如果你的 go 版本在 1.17 以下使用此命令安装：go get -u github.com/mozillazg/go-pinyin/cli/pinyin。1.17 及以上版本使用此命令安装：go install github.com/mozillazg/go-pinyin/cli/pinyin@latest。
使用 接下来将分别介绍 cli 的使用和 API 的使用。
cli 使用 安装完在终端输入 pinyin，可以看到使用的方法，尝试一个汉字，可以看到相应的拼音，但也可以看出对多音字的支持有问题。 $ pinyin 中国 zhōng guó $ pinyin 重庆 zhòng qìng 接下来介绍 API 的使用。
api 使用 通过查看文档，可以看出主要是 2 个方法 pinyin.NewArgs 和 pinyin.Pinyin 。
pinyin.NewArgs 创建包含默认配置的 Args, 可以通过修改 Args 的成员来使用不同的模式。
type Args struct { Style int // 拼音风格（默认：Normal) Heteronym bool // 是否启用多音字模式（默认：禁用） Separator string // Slug 中使用的分隔符（默认：-) // 处理没有拼音的字符（默认忽略没有拼音的字符） // 函数返回的 slice 的长度为 0 则表示忽略这个字符 Fallback func(r rune, a Args) \[\]string } pinyin.Pinyin 就是将汉字转为拼音。
...

 [post link to go 汉字转拼音 go-pinyin](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/)

前言 今天介绍一个 go 库 - mergo, mergo 用来方便的合并 struct 和 map ,可以将结构体的字段赋值到 map 中，可以将 map 的值赋值给结构体的字段。
Mergo 通过在零值字段中设置默认值来合并同类型的 struct 和 map。Mergo 不会合并未导出（私有）字段。它会递归合并任何已导出的字段。它也不会合并 map 中的结构体（因为它们无法使用 Go 反射寻址）。
Mergo 在很多知名项目中被使用，如 containerd、k8s、loki 等。
安装 使用以下命令安装 mergo : go get -u dario.cat/mergo
使用 接下来介绍 mergo 的基础使用和高级用法。
基础使用 mergo 提供了 2 个主要函数：Merge 和 Map, Mergo 用来合并 2 个相同结构的 struct 和 map, Map 用来在结构和 map 之间赋值。
例子：
package main import ( "fmt" "log" "github.com/imdario/mergo" ) type redisConfig struct { Address string Port int DB int UserName string PassWord string } var defaultConfig = redisConfig{ Address: "127.0.0.1", Port: 6379, DB: 1, UserName: "123", PassWord: "123", } func main() { var config redisConfig if err := mergo.Merge(&config, defaultConfig); err != nil { log.Fatal(err) } fmt.Println("redis address: ", config.Address) fmt.Println("redis port: ", config.Port) fmt.Println("redis db: ", config.DB) fmt.Println("redis username: ", config.UserName) fmt.Println("redis password: ", config.PassWord) var m = make(map\[string\]interface{}) if err := mergo.Map(&m, defaultConfig); err != nil { log.Fatal(err) } fmt.Println(m) } 接下来介绍一些高级用法：
...

 [post link to mergo 介绍](https://jasminides.com/posts/mergo_desc/)

前言 本文介绍 conc - 一个更好的 go 并发库，sourcegraph 在日常开发中使用 go 原生并发出现了问题，由此开发了 conc，相比标准并发代码更优雅，代码更少，下面展示一个例子，可以看出代码减少了许多。
type propagatedPanic struct { val any stack \[\]byte } func main() { done := make(chan \*propagatedPanic) go func() { defer func() { if v := recover(); v != nil { done <- &propagatedPanic{ val: v, stack: debug.Stack(), } } else { done <- nil } }() doSomethingThatMightPanic() }() if val := <-done; val != nil { panic(val) } } // conc func main() { var wg conc.WaitGroup wg.Go(doSomethingThatMightPanic) // panics with a nice stacktrace wg.Wait() } 安装 使用以下命令进行安装：go get github.com/sourcegraph/conc
...

 [post link to conc 一个更好的 go 并发库](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/)

前言 在 7 月份 go 团队正式推出了官方的漏洞检测工具 - govulncheck, govulncheck 默认向 https://vuln.go.dev/ 漏洞数据库请求，对数据库的请求不包含代码只有使用的包，你也可以使用 -db 来指导所使用的漏洞数据库，所使用的数据库必须实现相应的规范。
govulncheck 具有以下限制：
Govulncheck 在分析函数指针和接口调用时采用保守的方法，这可能导致一些情况下的误报或不准确的调用堆栈。 使用 reflect 进行的函数调用对于静态分析是不可见的。仅通过这些调用才能访问的易受攻击的代码将不会被报告。使用 unsafe 包可能导致漏报。 由于 Go 二进制文件不包含详细的调用信息，govulncheck 无法显示检测到的漏洞的调用图。对于二进制文件中但无法访问的代码，它可能还会报告误报。 目前还不支持 silencing 漏洞发现。请参阅 https://go.dev/issue/61211。 Govulncheck 只能读取使用 Go 1.18 及更高版本编译的二进制文件。 对于无法提取符号信息的二进制文件，govulncheck 会报告二进制文件所依赖的所有模块的漏洞。 govulncheck 架构图
govulncheck 还提供了一个可用的 API govulncheck，使开发者能够方便的将 govulncheck 集成到各种工具之中。
安装 通过以下命令安装 govulncheck:
go install golang.org/x/vuln/cmd/govulncheck@latest 使用 安装完 govulncheck 后，我们就可以使用了，进入项目路径中，执行 govulncheck ./... 。
以下是我的一个项目的输出：
Scanning your code and 508 packages across 71 dependent modules for known vulnerabilities... Vulnerability #1: GO-2023-2102 HTTP/2 rapid reset can cause excessive work in net/http More info: https://pkg.go.dev/vuln/GO-2023-2102 Standard library Found in: net/http@go1.21 Fixed in: net/http@go1.21.3 Example traces found: #1: cmd\\xxx\\main.go:94:19: xxx.main calls kratos.App.Run, which eventually calls http.Server.Serve #2: cmd\\xxx\\main.go:94:19: xxx.main calls kratos.App.Run, which eventually calls http.Server.ServeTLS Vulnerability #2: GO-2023-2043 Improper handling of special tags within script contexts in html/template More info: https://pkg.go.dev/vuln/GO-2023-2043 Standard library Found in: html/template@go1.21 Fixed in: html/template@go1.21.1 Example traces found: #1: cmd\\xxx\\main.go:94:19: xxx.main calls kratos.App.Run, which eventually calls template.Template.Execute #2: cmd\\xxx\\main.go:94:19: xxx.main calls kratos.App.Run, which eventually calls template.Template.ExecuteTemplate Vulnerability #3: GO-2023-2041 Improper handling of HTML-like comments in script contexts in html/template More info: https://pkg.go.dev/vuln/GO-2023-2041 Standard library Found in: html/template@go1.21 Fixed in: html/template@go1.21.1 Example traces found: #1: cmd\\xxx\\main.go:94:19: xxx.main calls kratos.App.Run, which eventually calls template.Template.Execute #2: cmd\\xxx\\main.go:94:19: xxx.main calls kratos.App.Run, which eventually calls template.Template.ExecuteTemplate === Informational === Found 3 vulnerabilities in packages that you import, but there are no call stacks leading to the use of these vulnerabilities. You may not need to take any action. See https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck for details. Vulnerability #1: GO-2023-2045 Memory exhaustion in QUIC connection handling in crypto/tls More info: https://pkg.go.dev/vuln/GO-2023-2045 Standard library Found in: crypto/tls@go1.21 Fixed in: crypto/tls@go1.21.1 Vulnerability #2: GO-2023-2044 Panic when processing post-handshake message on QUIC connections in crypto/tls More info: https://pkg.go.dev/vuln/GO-2023-2044 Standard library Found in: crypto/tls@go1.21 Fixed in: crypto/tls@go1.21.1 Vulnerability #3: GO-2023-1988 Improper rendering of text nodes in golang.org/x/net/html More info: https://pkg.go.dev/vuln/GO-2023-1988 Module: golang.org/x/net Found in: golang.org/x/net@v0.9.0 Fixed in: golang.org/x/net@v0.13.0 Your code is affected by 3 vulnerabilities from the Go standard library. Share feedback at https://go.dev/s/govulncheck-feedback. 输出内容分为 2 块，第一块是 Vulnerability 信息，是项目中存在的漏洞，可以看到发现了 3 个漏洞及具体的原因、触发函数、发现的版本和修复的版本。第二块是 Informational 是一些没有直接引用的包中存在的安全漏洞。
...

 [post link to Go 漏洞管理工具 govulncheck](https://jasminides.com/posts/go%E6%BC%8F%E6%B4%9E%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7-govulncheck/)

最近在实现一个功能时需要使用第三方的接口，由于第三方只提供了一个 WSDL 文件的链接，于是研究了 golang 如何解析 WSDL 并调用相应接口，本文就是介绍 WSDL 和 go 如何解析并调用。
WSDL 介绍 WSDL 是 Web Services Description Language（Web 服务描述语言）的缩写。它是一种用于描述基于 Web 服务的通信协议和消息格式的 XML 格式语言。
WSDL 被广泛用于描述 Web 服务的接口和操作。它定义了 Web 服务所提供的功能、方法、参数、数据类型以及与服务进行交互的方式。通过 WSDL 文件，客户端应用程序可以了解如何与特定的 Web 服务进行通信。
WSDL 文件通常包含以下几个主要部分：
服务定义：描述了 Web 服务的名称、命名空间和位置。 类型定义：定义了 Web 服务中使用的数据类型，例如字符串、整数等。 消息定义：定义了 Web 服务中使用的消息格式，包括输入和输出消息。 操作定义：定义了 Web 服务的操作或方法，包括输入和输出消息以及相关的参数。 绑定定义：定义了 Web 服务使用的通信协议和消息格式，例如 SOAP（Simple Object Access Protocol）和 HTTP（Hypertext Transfer Protocol）。 服务定义：将服务、绑定和端口等部分组合在一起，定义了 Web 服务的完整描述。 使用 WSDL，开发人员可以生成客户端代码，使其能够与 Web 服务进行交互。客户端可以根据 WSDL 文件了解 Web 服务的结构和可用方法，以便正确地构造请求和解析响应。
总之，WSDL 是一种用于描述 Web 服务接口和操作的语言，它提供了一种标准化的方式来描述和访问 Web 服务。
...

 [post link to Go WSDL](https://jasminides.com/posts/go-wdsl/)

以前的文章介绍了 chromedp 进行浏览器网页截图，这次介绍一种新的网页截图的方法——即使用 playwright 进行浏览器网页截图。
playwright 介绍 Playwright 是一个用于自动化浏览器操作的开源工具集。它由微软开发并于 2020 年发布，旨在提供一种跨浏览器、跨平台的解决方案，可用于测试 Web 应用程序、编写爬虫、执行自动化任务等。
Playwright 支持多种主流浏览器，包括 Chrome、Firefox、Safari 和 Edge，它提供了一组简单易用的 API，可以模拟用户与 Web 页面的交互行为，例如点击、填写表单、导航等。与其他类似工具相比，Playwright 的一个重要特点是它的跨浏览器支持，这意味着你可以使用相同的代码在不同浏览器上运行你的自动化任务，而不需要为每个浏览器单独编写代码。
Playwright 还提供了强大的调试功能，可以帮助开发人员在自动化过程中定位和解决问题。它支持截图和录制操作，使得调试变得更加直观和高效。
另外，Playwright 还具有一些高级功能，例如可以模拟不同的设备、网络环境和地理位置，以及支持并发执行多个浏览器实例等，这些功能使得它在编写复杂的自动化任务时非常有用。
由于我日常主要使用 go 语言进行开发，所以本文的内容主要以 playwright 的 go 模块 playwright-go 为主要介绍。
安装 go get -u github.com/playwright-community/playwright-go 安装相关浏览器和操作系统依赖项：
go run github.com/playwright-community/playwright-go/cmd/playwright@latest install --with-deps # Or go install github.com/playwright-community/playwright-go/cmd/playwright@latest playwright install --with-deps 也可以在代码中使用以下代码安装：err := playwright.Install()
通过安装截图可以看出安装了 3 大主流浏览器和 ffmpeg。
例子 接下来我们看一个官方的例子，从 Hacker News 中抓取当前投票最高的项目。
package main import ( "fmt" "log" "github.com/playwright-community/playwright-go" ) func main() { pw, err := playwright.Run() if err != nil { log.Fatalf("could not start playwright: %v", err) } browser, err := pw.Chromium.Launch() if err != nil { log.Fatalf("could not launch browser: %v", err) } page, err := browser.NewPage() if err != nil { log.Fatalf("could not create page: %v", err) } if \_, err = page.Goto("https://news.ycombinator.com"); err != nil { log.Fatalf("could not goto: %v", err) } entries, err := page.Locator(".athing").All() if err != nil { log.Fatalf("could not get entries: %v", err) } for i, entry := range entries { title, err := entry.Locator("td.title > span > a").TextContent() if err != nil { log.Fatalf("could not get text content: %v", err) } fmt.Printf("%d: %s\\n", i+1, title) } if err = browser.Close(); err != nil { log.Fatalf("could not close browser: %v", err) } if err = pw.Stop(); err != nil { log.Fatalf("could not stop Playwright: %v", err) } } ...

 [post link to playwright-go 浏览器截图](https://jasminides.com/posts/playwright-go%E7%AE%80%E4%BB%8B/) [Go to Top (Alt + G)](https://jasminides.com/tags/golang/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201736&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fgolang%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801869900&bpp=3&bdt=245&idt=75&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=5544689232868&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95355339%2C95340253%2C95340255&oid=2&pvsid=4225778809715555&tmod=311118106&uas=0&nvt=1&fsapi=1&fc=1920&brdim=160%2C160%2C160%2C160%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=97)

[iframe](https://ep2.adtrafficquality.google/sodar/sodar2/232/runner.html)[iframe](https://www.google.com/recaptcha/api2/aframe)[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Email Processing with Go
前言 电子邮件是现代办公和通信中不可或缺的工具，它广泛应用于数据交换和工作沟通。为了更高效地处理邮件内容，我们可以借助程序来实现自动化处理。本文将详细介绍如何使用 Go 语言来接收和处理电子邮件。
通过查阅资料，了解到可以通过 IMAP 协议来接收电子邮件，IMAP 协议是电子邮件接收协议，它允许客户端通过网络连接到邮件服务器，并从服务器上下载邮件。除了 IMAP 协议，还有 POP3 协议，POP3 协议与 IMAP 协议类似，但它在在客户端上对邮件的操作不会反馈到邮件服务器上，也就是说，在客户端的操作不会影响服务器上的邮件。当你需要从多个邮件客户端访问邮件时，IMAP 协议是一个更好的选择。
go-imap 通过对比不同的库，最后选择了 go-imap 库，它是一个基于 IMAP 协议的 Go 语言库，可以通过它构建客户端或者服务端。
安装 可以通过以下命令安装：
go get github.com/emersion/go-imap 使用 我们将通过官方的例子进行切入：
先通过 DialTLS 连接对应的电子邮箱 IMAP 服务器，然后通过登录邮箱，获取所有的邮箱文件夹，最后选择收件箱，获取收件箱中最新的 4 封邮件，并打印没封邮件的主题。
运行代码：
2024/11/23 16:16:11 Connecting to server... 2024/11/23 16:16:11 Connected 2024/11/23 16:16:12 Logged in 2024/11/23 16:16:12 Mailboxes: 2024/11/23 16:16:13 \* 其他文件夹 2024/11/23 16:16:13 \* Drafts 2024/11/23 16:16:13 \* Deleted Messages 2024/11/23 16:16:13 \* Sent Messages 2024/11/23 16:16:13 \* Junk 2024/11/23 16:16:13 \* INBOX 2024/11/23 16:16:13 Flags for INBOX: \[\\Answered \\Flagged \\Deleted \\Draft \\Seen\] 2024/11/23 16:16:13 Last 4 messages: 2024/11/23 16:16:13 \* =?GBK?B?xx?= 2024/11/23 16:16:13 \* =?GBK?B?xxx?= 2024/11/23 16:16:13 \* =?GBK?B?xx==?= 2024/11/23 16:16:13 \* =?GBK?B?xx+k=?= 2024/11/23 16:16:13 Done! 可以看到打印出来的邮件主题是乱码，通过查询资料，了解到邮件的字段是采用特殊编码的，需要进行解码。可以通过 https://github.com/emersion/go-message 这个库进行解码。
...

 [post link to Go Recivie Email](https://jasminides.com/posts/go-recivie-email/) [Go to Top (Alt + G)](https://jasminides.com/tags/imap/#top "Go to Top (Alt + G)")

## Using go-soap Library
目录

- [前言](https://jasminides.com/posts/go-soap-desc/#%e5%89%8d%e8%a8%80)
- [安装](https://jasminides.com/posts/go-soap-desc/#%e5%ae%89%e8%a3%85)
- [使用](https://jasminides.com/posts/go-soap-desc/#%e4%bd%bf%e7%94%a8)
- [不足](https://jasminides.com/posts/go-soap-desc/#%e4%b8%8d%e8%b6%b3)
- [参考](https://jasminides.com/posts/go-soap-desc/#%e5%8f%82%e8%80%83)

## 前言

最近需要调用一个第三方的接口进行数据的采集，这个接口是基于 SOAP 协议的，所以需要使用 soap 相关的客户端进行调用。于是我调研了一些开源的 golang 的 soap 客户端，发现 go-soap 这个库的文档比较完善，而且使用起来也比较简单，所以就选择了这个库。

## 安装

使用以下命令进行安装：

```bash
go get github.com/tiaguinho/gosoap

```

复制

## 使用

由于目前没有特别好的例子，这里就以官方的例子进行说明。

官方的代码如下：

```go
package main

import (
	"encoding/xml"
	"log"
	"net/http"
	"time"

	"github.com/tiaguinho/gosoap"
)

// GetIPLocationResponse will hold the Soap response
type GetIPLocationResponse struct {
	GetIPLocationResult string `xml:"GetIpLocationResult"`
}

// GetIPLocationResult will
type GetIPLocationResult struct {
	XMLName xml.Name `xml:"GeoIP"`
	Country string   `xml:"Country"`
	State   string   `xml:"State"`
}

var (
	r GetIPLocationResponse
)

func main() {
	httpClient := &http.Client{
		Timeout: 1500 * time.Millisecond,
	}
	soap, err := gosoap.SoapClient("http://wsgeoip.lavasoft.com/ipservice.asmx?WSDL", httpClient)
	if err != nil {
		log.Fatalf("SoapClient error: %s", err)
	}

	// Use gosoap.ArrayParams to support fixed position params
	params := gosoap.Params{
		"sIp": "8.8.8.8",
	}

	res, err := soap.Call("GetIpLocation", params)
	if err != nil {
		log.Fatalf("Call error: %s", err)
	}

	res.Unmarshal(&r)

	// GetIpLocationResult will be a string. We need to parse it to XML
	result := GetIPLocationResult{}
	err = xml.Unmarshal([]byte(r.GetIPLocationResult), &result)
	if err != nil {
		log.Fatalf("xml.Unmarshal error: %s", err)
	}

	if result.Country != "US" {
		log.Fatalf("error: %+v", r)
	}

	log.Println("Country: ", result.Country)
	log.Println("State: ", result.State)
}

```

复制

可以看到 go-soap 的使用跟常规的 http client 的使用方法类似，都是创建一个连接，准备方法的参数，然后调用相应的方法。
这段代码展示了如何使用 go-soap 库连接 SOAP 服务、发送请求、处理响应，以及如何解析 XML 格式的返回数据。

## 不足

在测试 go-soap 的过程中，发现 go-soap 缺少了一些功能，比如：接口鉴权功能，现在的一些接口都需要鉴权，go-soap 目前没有提供鉴权的功能，需要自己实现。

除了使用 go-soap 之外，还可以手动 使用 http 库进行调用，但是这样需要自己处理一些细节，比如：请求头，请求体，响应体等，比较麻烦。所以如果需要调用 soap 服务的话，建议使用 go-soap 库。

## 参考

- [https://github.com/tiaguinho/gosoap](https://github.com/tiaguinho/gosoap)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fgo-soap-desc%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/go-soap-desc/#top "Go to Top (Alt + G)")

## Go-SOAP Client Guide
前言 最近需要调用一个第三方的接口进行数据的采集，这个接口是基于 SOAP 协议的，所以需要使用 soap 相关的客户端进行调用。于是我调研了一些开源的 golang 的 soap 客户端，发现 go-soap 这个库的文档比较完善，而且使用起来也比较简单，所以就选择了这个库。
安装 使用以下命令进行安装：
go get github.com/tiaguinho/gosoap 使用 由于目前没有特别好的例子，这里就以官方的例子进行说明。
官方的代码如下：
package main import ( "encoding/xml" "log" "net/http" "time" "github.com/tiaguinho/gosoap" ) // GetIPLocationResponse will hold the Soap response type GetIPLocationResponse struct { GetIPLocationResult string \`xml:"GetIpLocationResult"\` } // GetIPLocationResult will type GetIPLocationResult struct { XMLName xml.Name \`xml:"GeoIP"\` Country string \`xml:"Country"\` State string \`xml:"State"\` } var ( r GetIPLocationResponse ) func main() { httpClient := &http.Client{ Timeout: 1500 \* time.Millisecond, } soap, err := gosoap.SoapClient("http://wsgeoip.lavasoft.com/ipservice.asmx?WSDL", httpClient) if err != nil { log.Fatalf("SoapClient error: %s", err) } // Use gosoap.ArrayParams to support fixed position params params := gosoap.Params{ "sIp": "8.8.8.8", } res, err := soap.Call("GetIpLocation", params) if err != nil { log.Fatalf("Call error: %s", err) } res.Unmarshal(&r) // GetIpLocationResult will be a string. We need to parse it to XML result := GetIPLocationResult{} err = xml.Unmarshal(\[\]byte(r.GetIPLocationResult), &result) if err != nil { log.Fatalf("xml.Unmarshal error: %s", err) } if result.Country != "US" { log.Fatalf("error: %+v", r) } log.Println("Country: ", result.Country) log.Println("State: ", result.State) } 可以看到 go-soap 的使用跟常规的 http client 的使用方法类似，都是创建一个连接，准备方法的参数，然后调用相应的方法。 这段代码展示了如何使用 go-soap 库连接 SOAP 服务、发送请求、处理响应，以及如何解析 XML 格式的返回数据。
...

 [post link to go-soap 简介](https://jasminides.com/posts/go-soap-desc/) [Go to Top (Alt + G)](https://jasminides.com/tags/soap/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fsoap%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801869821&bpp=2&bdt=168&idt=74&shv=r20250319&mjsv=m202503190101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=8233983412271&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95353420%2C31091178&oid=2&pvsid=3283386781894175&tmod=951257784&uas=0&nvt=1&fsapi=1&fc=1920&brdim=80%2C80%2C80%2C80%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=90)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Docker Configuration Guide
前言 最近遇到 Docker Desktop 构建 node 项目时，由于网络问题导致的构建失败问题，本文将介绍两个给 Docker Desktop 设置网络代理的方法。
修改 WSL2 配置 为了测试代理的效果，这里创建一个 go 服务，代码很简单，就是访问 https://www.google.com/ 并返回结果。如果能正常访问，说明代理设置成功。
package main import "net/http" func main() { resp, err := http.Get("https://www.google.com/") if err != nil { panic(err) } defer resp.Body.Close() println(resp.Status) } 第一种方法是修改 WSL2 的配置，在 windows C:\\Users<your\_username> 目录下创建 .wslconfig 文件，输入以下内容：
\[experimental\] autoMemoryReclaim=gradual networkingMode=mirrored dnsTunneling=true firewall=true autoProxy=true 然后重启 WSL: wsl --shutdown
networkingMode 为 mirrored 表示网络模式使用镜像模式，会镜像宿主机的网络设置，能更好的集成宿主机和 WSL 的网络。
autoProxy 开启了自动代理的功能，意味 WSL 自动配置代理设置。
配置好，我们构建 Docker 镜像，运行：
可以看到代理成功生效，可以正常访问。
...

 [post link to Docker Desktop 设置网络代理](https://jasminides.com/posts/docker-desktop-proxy/)

前言 Docker 是一个广受欢迎的开发平台，它允许用户通过容器化技术来构建、打包和部署应用程序。尽管 Docker 提供了强大的功能和灵活性，但对于初学者而言，在项目中配置 Docker 可能会遇到一些挑战。
不过，Docker 官方为了降低使用门槛，推出了一个便捷的命令docker init。这个命令旨在快速初始化 Docker 配置，从而简化将 Docker 集成到项目中的流程。通过使用这个命令，用户可以轻松地为项目设置必要的 Docker 支持，进而享受到 Docker 带来的便利和效率提升。
docker init 简介 docker init 命令会根据用户指定的选项生成运行容器的一些文件，极大的加快了项目的容器化：
.dockerignore : docker 构建时忽略的文件列表 Dockerfile: 镜像的核心文件 Compose.yaml: docker compose 的配置文件 README.Docker.md 如果你的项目中已有以上文件，会让你选择是否覆盖旧文件避免文件冲突问题。
docker init 提供了一组项目的模板文件，包括了 Go、Python、ASP.NET Core 等常见的服务器应用程序及一个其它类型应用程序模板。开发者使用 init 命令时，可以根据选择的模板生成相应的文件，使开发者可以快速的构建并启动容器。
使用 接下来介绍如何使用 docker init 进行项目容器的初始化，这里以前文的 go 项目为例子进行介绍。
进入项目根目录执行 init 命令，选择 go 模板，会让你选择使用的 go 版本，主程序的位置及应用所使用的端口： 执行完可以看到会生成相应的文件及如何构建并运行的命令。
查看生成的 Dockerfile 和 Compose.yaml 文件：
\# syntax=docker/dockerfile:1 # Comments are provided throughout this file to help you get started. # If you need more help, visit the Dockerfile reference guide at # https://docs.docker.com/go/dockerfile-reference/ # Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7 ################################################################################ # Create a stage for building the application. ARG GO\_VERSION=1.21.0 FROM --platform=$BUILDPLATFORM golang:${GO\_VERSION} AS build WORKDIR /src # Download dependencies as a separate step to take advantage of Docker's caching. # Leverage a cache mount to /go/pkg/mod/ to speed up subsequent builds. # Leverage bind mounts to go.sum and go.mod to avoid having to copy them into # the container. RUN --mount=type=cache,target=/go/pkg/mod/ \ --mount=type=bind,source=go.sum,target=go.sum \ --mount=type=bind,source=go.mod,target=go.mod \ go mod download -x # This is the architecture you’re building for, which is passed in by the builder. # Placing it here allows the previous steps to be cached across architectures. ARG TARGETARCH # Build the application. # Leverage a cache mount to /go/pkg/mod/ to speed up subsequent builds. # Leverage a bind mount to the current directory to avoid having to copy the # source code into the container. RUN --mount=type=cache,target=/go/pkg/mod/ \ --mount=type=bind,target=. \ CGO\_ENABLED=0 GOARCH=$TARGETARCH go build -o /bin/server ./retry/server ################################################################################ # Create a new stage for running the application that contains the minimal # runtime dependencies for the application. This often uses a different base # image from the build stage where the necessary files are copied from the build # stage. # # The example below uses the alpine image as the foundation for running the app. # By specifying the "latest" tag, it will also use whatever happens to be the # most recent version of that image when you build your Dockerfile. If # reproducability is important, consider using a versioned tag # (e.g., alpine:3.17.2) or SHA (e.g., alpine@sha256:c41ab5c992deb4fe7e5da09f67a8804a46bd0592bfdf0b1847dde0e0889d2bff). FROM alpine:latest AS final # Install any runtime dependencies that are needed to run your application. # Leverage a cache mount to /var/cache/apk/ to speed up subsequent builds. RUN --mount=type=cache,target=/var/cache/apk \ apk --update add \ ca-certificates \ tzdata \ && \ update-ca-certificates # Create a non-privileged user that the app will run under. # See https://docs.docker.com/go/dockerfile-user-best-practices/ ARG UID=10001 RUN adduser \ --disabled-password \ --gecos "" \ --home "/nonexistent" \ --shell "/sbin/nologin" \ --no-create-home \ --uid "${UID}" \ appuser USER appuser # Copy the executable from the "build" stage. COPY --from=build /bin/server /bin/ # Expose the port that the application listens on. EXPOSE 9000 # What the container should run when it is started. ENTRYPOINT \[ "/bin/server" \] 可以看到 Dockerfile 是一个常见的多阶段构建镜像流程。
...

 [post link to docker init 命令](https://jasminides.com/posts/docker_init_command/)

最近在学习常用的容器运行时 containerd, 本篇我就来介绍如何本地构建 containerd 进行调试开发，主要介绍 2 种 常规方式和使用容器构建，由于本地环境限制，我主要是使用 docker 搭建本地调试环境。
非容器 build 这里先开始介绍常规直接从源码本地构建的方式。
构建环境要求 1 go1.19.x 及以上版本
2 Protoc 3.x+
3 适用于您的发行版的 Btrfs 标头和库。请注意，可以通过构建标签禁用构建 btrfs 驱动程序 no\_btrfs，从而删除此依赖项。
前面 2 点相信大家都很清楚，第三点的 Btrfs 是什么呢？Btrfs 是一种现代的 Linux 写时复制（COW）文件系统，旨在实现先进的功能，同时也注重容错、修复和简易管理。
build 1 拉取 containerd 源代码至本地
2 构建
进入源代码根目录，执行一下命令：
cd containerd make 执行后，会在 ./bin/ 目录下生成所有项目的二进制文件。
如果你需要修改 gRPC API ,修改后需要使用 protoc 编译生成新的代码：make generate
docker 容器构建 接下来讲解怎么通过 docker 构建本地 containerd 调试环境。
构建要求 1 go1.19.x 及以上版本
2 Protoc 3.x+
...

 [post link to Containerd 本地调试环境搭建](https://jasminides.com/posts/containerd%E6%9C%AC%E5%9C%B0%E8%B0%83%E8%AF%95%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA/)

问题 最近在使用 MinIO SDK 上传资源对象时，出现了一个问题：The difference between the request time and the server's time is too large. 从错误信息可以看出客户端上传资源的时间与 Minio server 的时间相差太大，导致资源上传失败。
解决 根据错误信息得出 server 端的时间出现异常，由于我采用容器部署的方式，因此可以先查看容器的时间是否正确。
进入 Minio 容器 , 执行命令：date, 可以看到如图结果 ( UTC 时间): 而目前的时间是 ( CST 时间) :
可以看出容器的时间与实际的时间相差太大，所以导致资源上传失败。
方法 1 出现了时间异常的问题，可能很多人第一反应就是调整容器的时间，通过 ntpdate 等工具调整时间，这种解决方法方法适用于非容器的 MinIO SERVER 环境调整时间，容器因为一些限制无法使用此方法。
方法 2 在网上查看了许多相关的问题，有了一个针对容器的解决方法，执行：
docker run --rm --privileged alpine hwclock -s 可以看到容器时间已经正常了：
我对这条命令不太明白，不明白为什么会影响到其它运行中的容器，可能是与 docker for win 的一些容器实现机制相关。
参考资料 https://stackoverflow.com/questions/4770635/s3-error-the-difference-between-the-request-time-and-the-current-time-is-too-la https://www.cnblogs.com/ryanlamp/p/13387358.html https://github.com/minio/minio-java/issues/701

 [post link to 容器出现时间异常问题及解决方法](https://jasminides.com/posts/%E5%AE%B9%E5%99%A8%E5%87%BA%E7%8E%B0%E6%97%B6%E9%97%B4%E5%BC%82%E5%B8%B8%E9%97%AE%E9%A2%98%E5%8F%8A%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95/)

Docker grafana 启动失败 今天在使用 Docker 启动 grafana 的时候，遇到了一个问题，问题如图： 为什么会出现这个问题 根据错误日志的提示，打开 http://docs.grafana.org/installation/docker/#migrate-to-v51-or-later 网址，根据官方的描述，grafana Docker 镜像在版本 5.1 及以后有了重大改变：
\\* 在容器启动过程中不会改变文件的权限 \\* 默认用户 ID 由 104 变为 472 \* 删除了以下的隐式卷： \* /var/lib/grafana \* /etc/grafana \* /var/log/grafana 解决 根据官方文档的提示，我仔细查看了我的 compose 文件，发现我加了 user: ‘104’ , 应该是此行的原因导致 grafana 没有启动成功，删除此行，顺利启动。

 [post link to Docker_grafana 启动失败](https://jasminides.com/posts/docker_grafana%E5%90%AF%E5%8A%A8%E5%A4%B1%E8%B4%A5/)

Nginx 搭建静态图片资源服务器 本文介绍使用 Docker Nginx 搭建静态图片资源服务器的过程和搭建中间遇到的问题。
我使用 Docker compose 搭建静态图片资源服务器，我使用的 compose 文件内容如下：
version: '3.1' services: nginx: restart: always image: nginx container\_name: asset ports: - 80:80 volumes: - ./nginx.conf:/etc/nginx/nginx.conf - ./uploads:/usr/share/nginx/uploads - ./conf.d:/etc/nginx/conf.d /srv/msg/storage/uploads:/usr/share/nginx/uploads 将本地的图片文件夹挂载到容器内的 /usr/share/nginx/uploads 文件夹 nginx.conf 是 Nginx 的主配置文件，conf.d 是各个网站配置的文件夹。我的 nginx.conf 内容如下：
user nginx; worker\_processes 1; error\_log /var/log/nginx/error.log warn; pid /var/run/nginx.pid; events { worker\_connections 1024; } http { include /etc/nginx/mime.types; default\_type application/octet-stream; log\_format main '$remote\_addr - $remote\_user \[$time\_local\] "$request" ' '$status $body\_bytes\_sent "$http\_referer" ' '"$http\_user\_agent" "$http\_x\_forwarded\_for"'; access\_log /var/log/nginx/access.log main; sendfile on; #tcp\_nopush on; keepalive\_timeout 65; include /etc/nginx/conf.d/\*.conf; server { listen 80 default\_server; listen \[::\]:80 default\_server; server\_name 192.168.1.117; root /usr/share/nginx/uploads/; location /{ autoindex on; } error\_page 404 /404.html; location = /40x.html { } error\_page 500 502 503 504 /50x.html; location = /50x.html { } } } 静态资源图片服务器的配置文件如下：
...

 [post link to Nginx 搭建静态图片资源服务器](https://jasminides.com/posts/nginx%E6%90%AD%E5%BB%BA%E9%9D%99%E6%80%81%E5%9B%BE%E7%89%87%E8%B5%84%E6%BA%90%E6%9C%8D%E5%8A%A1%E5%99%A8/)

Traefik 入门使用 简介 Traefik（发音为 traffic）是一个现代 HTTP 反向代理和负载均衡设施，使部署微服务变得容易。Traefik 与你现有的基础设施组件（Docker、Swarm 模式、Kubernetes、Consul、Etcd、…）集成，并自动和动态地配置自己。将 Traefik 指向你的基础设施组件应该是你唯一需要的配置步骤。
快速入门 在这里我使用 Docker 来快速使用 Traefik。
先创建一个 docker-compose.yml 文件，写入如下内容： version: '3' services: reverse-proxy: # 使用的 traefik2.4 Docker 镜像版本 image: traefik:v2.4 # 通过命令行参数启动 traefik，启用不安全模式以使用 dashboard，配置发现使用了 docker command: --api.insecure=true --providers.docker ports: # The HTTP port - "80:80" # dashboard 端口 - "8080:8080" volumes: # 监听 docker 事件 - /var/run/docker.sock:/var/run/docker.sock 执行 docker-compose up -d reverse-proxy 启动 docker-compose up -d reverse-proxy 打开浏览器输入 http://localhost:8080/api/rawdata 访问看见 Traefik’s API rawdata，就表示安装成功了。
...

 [post link to Traefik 入门使用](https://jasminides.com/posts/traefik%E5%85%A5%E9%97%A8%E4%BD%BF%E7%94%A8/)

Gitlab CI 构建 docker 镜像 利用 Gitlab CI 结合 Docker 构建 docker 镜像主要有三种方法。
将 Docker 执行器与 Docker 镜像一起使用。 使用 shell 执行器 Docker socket 绑定 现在来讲讲我的具体使用过程和遇到的一些问题，由于我的 gitlab-runners 使用了 docker 执行器，所以我主要使用了 1 和 3 两种方法。
由于网上的相关文章主要是采用 Docker in Docker 的方式，所以最开始我也是采用这种方式。 我的 ci 脚本是：
services: - docker:dind variables: OUTPUT\_NAME: bot DOCKER\_HOST: tcp://localhost:2375 DOCKER\_DRIVER: overlay2 DOCKER\_TLS\_CERTDIR: "" build\_docker\_image\_and\_push\_to\_nexus: stage: build image: docker:stable extends: .go-cache script: - docker info - docker build -t docker.overtsarry.vip/bot:1.0.1 . - docker login --username=$username docker.overtsarry.vip --password $pwd - docker push docker.overtsarry.vip/bot:1.0.1 运行 CI，发现 CI 运行失败，具体报错是
...

 [post link to Gitlab CI 构建 docker 镜像](https://jasminides.com/posts/gitlab-ci%E6%9E%84%E5%BB%BAdocker%E9%95%9C%E5%83%8F/) [Go to Top (Alt + G)](https://jasminides.com/tags/docker/#top "Go to Top (Alt + G)")

## Docker Desktop Proxy Setup
目录

- [前言](https://jasminides.com/posts/docker-desktop-proxy/#%e5%89%8d%e8%a8%80)
- [修改 WSL2 配置](https://jasminides.com/posts/docker-desktop-proxy/#%e4%bf%ae%e6%94%b9-wsl2-%e9%85%8d%e7%bd%ae)
- [修改 Docker Desktop 配置](https://jasminides.com/posts/docker-desktop-proxy/#%e4%bf%ae%e6%94%b9-docker-desktop-%e9%85%8d%e7%bd%ae)
- [小结](https://jasminides.com/posts/docker-desktop-proxy/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/docker-desktop-proxy/#%e5%8f%82%e8%80%83)

## 前言

最近遇到 Docker Desktop 构建 node 项目时，由于网络问题导致的构建失败问题，本文将介绍两个给 Docker Desktop 设置网络代理的方法。

## 修改 WSL2 配置

为了测试代理的效果，这里创建一个 go 服务，代码很简单，就是访问 `https://www.google.com/` 并返回结果。如果能正常访问，说明代理设置成功。

```go
package main

import "net/http"

func main() {
	resp, err := http.Get("https://www.google.com/")
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	println(resp.Status)
}

```

复制

第一种方法是修改 WSL2 的配置，在 windows C:\\Users<your\_username> 目录下创建 .wslconfig 文件，输入以下内容：

```text
[experimental]
autoMemoryReclaim=gradual
networkingMode=mirrored
dnsTunneling=true
firewall=true
autoProxy=true

```

复制

然后重启 WSL: `wsl --shutdown`

networkingMode 为 mirrored 表示网络模式使用镜像模式，会镜像宿主机的网络设置，能更好的集成宿主机和 WSL 的网络。

autoProxy 开启了自动代理的功能，意味 WSL 自动配置代理设置。

配置好，我们构建 Docker 镜像，运行：

![wsl2 配置](https://jasminides.com/img/wsl-proxy/image.png)

可以看到代理成功生效，可以正常访问。

接下来介绍通过修改 Docker Desktop 的配置文件，设置代理。

## 修改 Docker Desktop 配置

打开 Docker Desktop 的设置，找到 Resources Proxies 选项，设置代理。

![alt text](https://jasminides.com/img/wsl-proxy/image-1.png)

运行 Docker 镜像，可以看到代理成功生效，可以正常访问。

## 小结

本文介绍了两种给 Docker Desktop 设置网络代理的方法，分别是修改 WSL2 配置和修改 Docker Desktop 配置。

## 参考

- [https://docs.docker.com/engine/network/drivers/host/#docker-desktop](https://docs.docker.com/engine/network/drivers/host/#docker-desktop)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fdocker-desktop-proxy%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/docker-desktop-proxy/#top "Go to Top (Alt + G)")

## Deploying Hugo on GitHub
前言 本文将介绍当初我搭建这个博客网站的时候，是如何将 Hugo 网站部署到 GitHub 上的，本文会采用与 hugo 官方不同的方式进行部署。
创建仓库 首先我们在 GitHub 上创建一个仓库，仓库名称为 username.github.io，其中 username 为你的 GitHub 用户名。这个仓库是用来存储 hugo 最终生成的静态网站文件的。再创建一个名称为 blogs 的仓库，这个仓库是用来存储 hugo 网站源内容文件的。
启用 GitHub Pages 在 username.github.io 仓库中，点击 Settings 选项卡，在 GitHub Pages 中选择 Source 为 从分支部署，然后点击 Save 按钮。
启用 GitHub Actions 接下来要实现提交 hugo 网站源文件到 blogs 仓库后，自动将 hugo 网站源文件编译成静态网站文件，并提交到 username.github.io 仓库中，这样就可以通过访问 username.github.io 仓库来访问 hugo 网站了。
生成 personal\_token 在配置 Actions 前，需要先生成 personal\_token，用于在 GitHub Actions 中使用。我们进入 Settings 选项卡，在 Developer settings 中选择 Personal access tokens，然后选择 Tokens (classic)，然后点击 Generate new token 下的Generate new token(classic)按钮，在 Note 中输入 blog，在 Expiration 中选择 No expiration，在 Select scopes 中选择 repo 和 admin:repo\_hook，然后点击 Generate token 按钮，生成 personal\_token。
...

 [post link to 如何在 Github Pages 上部署 Hugo 网站](https://jasminides.com/posts/hugo_deploy_github/) [Go to Top (Alt + G)](https://jasminides.com/tags/github-pages/#top "Go to Top (Alt + G)")

## Hugo GitHub Deployment
前言 本文将介绍当初我搭建这个博客网站的时候，是如何将 Hugo 网站部署到 GitHub 上的，本文会采用与 hugo 官方不同的方式进行部署。
创建仓库 首先我们在 GitHub 上创建一个仓库，仓库名称为 username.github.io，其中 username 为你的 GitHub 用户名。这个仓库是用来存储 hugo 最终生成的静态网站文件的。再创建一个名称为 blogs 的仓库，这个仓库是用来存储 hugo 网站源内容文件的。
启用 GitHub Pages 在 username.github.io 仓库中，点击 Settings 选项卡，在 GitHub Pages 中选择 Source 为 从分支部署，然后点击 Save 按钮。
启用 GitHub Actions 接下来要实现提交 hugo 网站源文件到 blogs 仓库后，自动将 hugo 网站源文件编译成静态网站文件，并提交到 username.github.io 仓库中，这样就可以通过访问 username.github.io 仓库来访问 hugo 网站了。
生成 personal\_token 在配置 Actions 前，需要先生成 personal\_token，用于在 GitHub Actions 中使用。我们进入 Settings 选项卡，在 Developer settings 中选择 Personal access tokens，然后选择 Tokens (classic)，然后点击 Generate new token 下的Generate new token(classic)按钮，在 Note 中输入 blog，在 Expiration 中选择 No expiration，在 Select scopes 中选择 repo 和 admin:repo\_hook，然后点击 Generate token 按钮，生成 personal\_token。
...

 [post link to 如何在 Github Pages 上部署 Hugo 网站](https://jasminides.com/posts/hugo_deploy_github/) [Go to Top (Alt + G)](https://jasminides.com/tags/hugo/#top "Go to Top (Alt + G)")

## Hugo Deployment Guide
目录

- [前言](https://jasminides.com/posts/hugo_deploy_github/#%e5%89%8d%e8%a8%80)
- [创建仓库](https://jasminides.com/posts/hugo_deploy_github/#%e5%88%9b%e5%bb%ba%e4%bb%93%e5%ba%93)
  - [启用 GitHub Pages](https://jasminides.com/posts/hugo_deploy_github/#%e5%90%af%e7%94%a8-github-pages)
  - [启用 GitHub Actions](https://jasminides.com/posts/hugo_deploy_github/#%e5%90%af%e7%94%a8-github-actions)
    - [生成 personal\_token](https://jasminides.com/posts/hugo_deploy_github/#%e7%94%9f%e6%88%90-personal_token)
    - [配置 personal\_token secret](https://jasminides.com/posts/hugo_deploy_github/#%e9%85%8d%e7%bd%ae-personal_token-secret)
    - [配置 GitHub Actions](https://jasminides.com/posts/hugo_deploy_github/#%e9%85%8d%e7%bd%ae-github-actions)
- [参考](https://jasminides.com/posts/hugo_deploy_github/#%e5%8f%82%e8%80%83)

## 前言

本文将介绍当初我搭建这个博客网站的时候，是如何将 Hugo 网站部署到 GitHub 上的，本文会采用与 hugo 官方不同的方式进行部署。

## 创建仓库

首先我们在 GitHub 上创建一个仓库，仓库名称为 `username.github.io`，其中 `username` 为你的 GitHub 用户名。这个仓库是用来存储 hugo 最终生成的静态网站文件的。再创建一个名称为 blogs 的仓库，这个仓库是用来存储 hugo 网站源内容文件的。

### 启用 GitHub Pages

在 `username.github.io` 仓库中，点击 `Settings` 选项卡，在 `GitHub Pages` 中选择 `Source` 为 从分支部署，然后点击 `Save` 按钮。

### 启用 GitHub Actions

接下来要实现提交 hugo 网站源文件到 `blogs` 仓库后，自动将 hugo 网站源文件编译成静态网站文件，并提交到 `username.github.io` 仓库中，这样就可以通过访问 `username.github.io` 仓库来访问 hugo 网站了。

#### 生成 personal\_token

在配置 Actions 前，需要先生成 personal\_token，用于在 GitHub Actions 中使用。我们进入 `Settings` 选项卡，在 `Developer settings` 中选择 `Personal access tokens`，然后选择 `Tokens (classic)`，然后点击 `Generate new token` 下的 `Generate new token(classic)` 按钮，在 `Note` 中输入 `blog`，在 `Expiration` 中选择 `No expiration`，在 `Select scopes` 中选择 `repo` 和 `admin:repo_hook`，然后点击 `Generate token` 按钮，生成 personal\_token。

保存好 personal\_token，后面会用到。

#### 配置 personal\_token secret

在 `blogs` 仓库中，点击 `Settings` 选项卡，在 `Secrets and variables` 中选择 `Actions`，然后点击 `New repository secret`，在 `Name` 中输入 `ACTION_ACCESS_TOKEN`，在 `Value` 中输入刚刚生成的 personal\_token，然后点击 `Add secret` 按钮。

#### 配置 GitHub Actions

在 `blogs` 仓库中，在 .github/workflows 目录下创建一个名为 `deploy.yml` 的 GitHub Actions 配置文件，内容如下：

```yaml
name: github pages # 名字自取

on:
  push:
    branches:
      - master  # 这里的意思是当 main 分支发生 push 的时候，运行下面的 jobs，这里先改为 github-actions

jobs:
  deploy: # 任务名自取
    runs-on: ubuntu-22.04	# 在什么环境运行任务
    steps:
      - uses: actions/checkout@v4	# 引用 actions/checkout 这个 action，与所在的 github 仓库同名
        with:
          submodules: true  # Fetch Hugo themes (true OR recursive) 获取 submodule 主题
          fetch-depth: 0    # Fetch all history for .GitInfo and .Lastmod

      - name: Setup Hugo	# 步骤名自取
        uses: peaceiris/actions-hugo@v3	# hugo 官方提供的 action，用于在任务环境中获取 hugo
        with:
          hugo-version: 'latest'	# 获取最新版本的 hugo
          # extended: true

      - name: Build
        run: hugo --minify	# 使用 hugo 构建静态网页

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3	# 一个自动发布 github pages 的 action
        with:
          # github_token: ${{ secrets.GITHUB_TOKEN }} 该项适用于发布到源码相同 repo 的情况，不能用于发布到其他 repo
          external_repository: overstarry/overstarry.github.io	# 发布到哪个 repo
          personal_token: ${{ secrets.ACTION_ACCESS_TOKEN }}	# 发布到其他 repo 需要提供上面生成的 personal access token
          publish_dir: ./public	# 注意这里指的是要发布哪个文件夹的内容，而不是指发布到目的仓库的什么位置，因为 hugo 默认生成静态网页到 public 文件夹，所以这里发布 public 文件夹里的内容
          publish_branch: master	# 发布到哪个 branch

```

复制

personal\_token 修改为刚刚配置的 personal\_token 名称，external\_repository 修改为 `username.github.io` 仓库的地址，publish\_branch 修改为 `username.github.io` 仓库的 branch。

截止到此，我们就实现了使用 Github Pages 部署 Hugo 网站。如果你想要使用自定义域名，可以参考 [Hugo Github Pages 自定义域名](https://overstarry.vip/posts/github_page%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%9F%E5%90%8D/) 进行配置。

如果你想将 hugo 网站部署到 cloudflare pages 上，可以参考 [Hugo Cloudflare Pages](https://developers.cloudflare.com/pages/framework-guides/deploy-a-hugo-site/) 进行配置。

## 参考

- [https://hugo.opendocs.io/hosting-and-deployment/hosting-on-github/](https://hugo.opendocs.io/hosting-and-deployment/hosting-on-github/)

- [https://pages.github.com/](https://pages.github.com/)

- [https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

- [https://overstarry.vip/posts/github\_page%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%9F%E5%90%8D/](https://overstarry.vip/posts/github_page%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%9F%E5%90%8D/)

- [https://developers.cloudflare.com/pages/framework-guides/deploy-a-hugo-site/](https://developers.cloudflare.com/pages/framework-guides/deploy-a-hugo-site/)


giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fhugo_deploy_github%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/hugo_deploy_github/#top "Go to Top (Alt + G)")

## v0.dev Chat Overview
v0.dev chat 介绍 v0.dev chat 是 vercel 推出的最新的生成式 AI 聊天机器人，可以通过用户对话的方式来生成相应的 react 代码。
v0.dev chat 相比 V0.dev 有以下优点：
最新的 react、next.js、web 技术知识 可以运行 npm 包 更快更可靠的流失传输 接下来将通过官方的几个例子及个人尝试的效果来讲解。
官方例子 解释 next 缓存机制 打开 https://v0.dev/chat/E8fIPvg，可以看到 bot 很好的通过图表及文字讲述了 next 的缓存机制。
贪吃蛇游戏 打开这个 https://v0.dev/chat/AjJVzgx，可以看到用户上传蛇的皮肤并一步步引导 bot 生成贪吃蛇游戏。
个人尝试 接下来将通过一个简单的视频网站例子来尝试 v0.dev chat 的效果。
先通过简单的提示生成视频网站的初始代码： 可以看到 bot 生成的代码是非常完整的，并且可以运行预览的。接下来继续完善视频网站。
接下来添加视频下载保存功能 接下来添加视频网站首页功能 通过不断的调整，可以慢慢的形成一个视频网站的雏形。
总结 v0.dev chat 可以很好的通过对话的方式来生成 react 代码，并且可以运行 npm 包，可以很好的帮助我们快速生成代码。本文通过构建一个视频网站的例子来尝试 v0.dev，由于免费版限制了 message 的数量，感兴趣的可以自行尝试。视频网站的生成步骤可以通过此链接查看：https://v0.dev/chat/PsqNuwjpzXx
...

 [post link to V0.dev chat](https://jasminides.com/posts/v0dev/) [Go to Top (Alt + G)](https://jasminides.com/tags/v0.dev/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fv0.dev%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801875894&bpp=3&bdt=214&idt=72&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=1370785727082&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95330276%2C95353450%2C31091145%2C95355300&oid=2&pvsid=4424771893632925&tmod=1151247953&uas=0&nvt=1&fsapi=1&fc=1920&brdim=90%2C90%2C90%2C90%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=90)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## v0.dev Chat Overview
目录

- [v0.dev chat 介绍](https://jasminides.com/posts/v0dev/#v0dev-chat-%e4%bb%8b%e7%bb%8d)
- [官方例子](https://jasminides.com/posts/v0dev/#%e5%ae%98%e6%96%b9%e4%be%8b%e5%ad%90)
  - [解释 next 缓存机制](https://jasminides.com/posts/v0dev/#%e8%a7%a3%e9%87%8a-next-%e7%bc%93%e5%ad%98%e6%9c%ba%e5%88%b6)
  - [贪吃蛇游戏](https://jasminides.com/posts/v0dev/#%e8%b4%aa%e5%90%83%e8%9b%87%e6%b8%b8%e6%88%8f)
- [个人尝试](https://jasminides.com/posts/v0dev/#%e4%b8%aa%e4%ba%ba%e5%b0%9d%e8%af%95)
- [总结](https://jasminides.com/posts/v0dev/#%e6%80%bb%e7%bb%93)
- [参考](https://jasminides.com/posts/v0dev/#%e5%8f%82%e8%80%83)

## v0.dev chat 介绍

v0.dev chat 是 vercel 推出的最新的生成式 AI 聊天机器人，可以通过用户对话的方式来生成相应的 react 代码。

v0.dev chat 相比 V0.dev 有以下优点：

- 最新的 react、next.js、web 技术知识
- 可以运行 npm 包
- 更快更可靠的流失传输

接下来将通过官方的几个例子及个人尝试的效果来讲解。

## 官方例子

### 解释 next 缓存机制

打开 [https://v0.dev/chat/E8fIPvg](https://v0.dev/chat/E8fIPvg)，可以看到 bot 很好的通过图表及文字讲述了 next 的缓存机制。

![alt text](https://jasminides.com/img/v0dev/image.png)

### 贪吃蛇游戏

打开这个 [https://v0.dev/chat/AjJVzgx](https://v0.dev/chat/AjJVzgx)，可以看到用户上传蛇的皮肤并一步步引导 bot 生成贪吃蛇游戏。

![alt text](https://jasminides.com/img/v0dev/image-1.png)

## 个人尝试

接下来将通过一个简单的视频网站例子来尝试 v0.dev chat 的效果。

1. 先通过简单的提示生成视频网站的初始代码：

![alt text](https://jasminides.com/img/v0dev/image-2.png)

可以看到 bot 生成的代码是非常完整的，并且可以运行预览的。接下来继续完善视频网站。

2. 接下来添加视频下载保存功能

![alt text](https://jasminides.com/img/v0dev/image-3.png)

3. 接下来添加视频网站首页功能

![alt text](https://jasminides.com/img/v0dev/image-4.png)

![alt text](https://jasminides.com/img/v0dev/image-5.png)

通过不断的调整，可以慢慢的形成一个视频网站的雏形。

## 总结

v0.dev chat 可以很好的通过对话的方式来生成 react 代码，并且可以运行 npm 包，可以很好的帮助我们快速生成代码。本文通过构建一个视频网站的例子来尝试 v0.dev，由于免费版限制了 message 的数量，感兴趣的可以自行尝试。视频网站的生成步骤可以通过此链接查看：https://v0.dev/chat/PsqNuwjpzXx

## 参考

- [https://v0.dev/chat](https://v0.dev/chat)

- [https://v0.dev/chat/E8fIPvg](https://v0.dev/chat/E8fIPvg)

- [https://v0.dev/chat/AjJVzgx](https://v0.dev/chat/AjJVzgx)

- [https://github.com/sharkqwy/v0prompt](https://github.com/sharkqwy/v0prompt)

- [https://v0.dev/chat/PsqNuwjpzXx](https://v0.dev/chat/PsqNuwjpzXx)


giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fv0dev%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/v0dev/#top "Go to Top (Alt + G)")

## Markdown Preview Enhanced Guide
前言 最近需要写总结报告，以前写总结报告时，往往使用 Word 进行编写，但由于显示排版等问题，本次采用了 Markdown 进行编写，在编写时使用了 Markdown Preview Enhanced 插件。本文介绍 Markdown Preview Enhanced 插件的安装及所使用的功能。
安装 打开 vscode 编辑器，打开扩展栏，输入 Markdown Preview Enhanced ,第一个就是，点击安装后即可。
功能介绍 接下来将介绍一些在编写文档中所使用的功能。
diagrams Markdown Preview Enhanced 插件支持 low charts, sequence diagrams, mermaid, PlantUML, WaveDrom, GraphViz，Vega & Vega-lite，Ditaa 图像渲染。
在文档中我使用了 mermaid 和 Vega-lite，Vega-lite 用于绘制图表，mermaid 用于绘制流程图。
接下来介绍 markdown 中如何使用 Vega-lite 绘制图表，使用以下代码即可绘制一个漂亮的饼图：
如果想要居中的效果，可以添加 {align="center"}来设置居中的效果。
mermaid 可以用来绘制流程图，使用以下代码即可绘制一个简单的流程图：
如果我们想要添加 css 效果该怎么办呢，可以通过 HTML + css 的形式来显示我们想要的效果：
...

 [post link to Markdown Preview Enhanced plugin introduction and simple use](https://jasminides.com/posts/markdown-preview-enhanced/) [Go to Top (Alt + G)](https://jasminides.com/tags/markdown/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fmarkdown%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801875878&bpp=3&bdt=181&idt=166&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=5381882784826&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95344791%2C31088249&oid=2&pvsid=516591884593658&tmod=322629664&uas=0&nvt=1&fsapi=1&fc=1920&brdim=80%2C80%2C80%2C80%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=183)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Markdown Preview Enhanced
目录

- [前言](https://jasminides.com/posts/markdown-preview-enhanced/#%e5%89%8d%e8%a8%80)
- [安装](https://jasminides.com/posts/markdown-preview-enhanced/#%e5%ae%89%e8%a3%85)
- [功能介绍](https://jasminides.com/posts/markdown-preview-enhanced/#%e5%8a%9f%e8%83%bd%e4%bb%8b%e7%bb%8d)
  - [diagrams](https://jasminides.com/posts/markdown-preview-enhanced/#diagrams)
- [小结](https://jasminides.com/posts/markdown-preview-enhanced/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/markdown-preview-enhanced/#%e5%8f%82%e8%80%83)

## 前言

最近需要写总结报告，以前写总结报告时，往往使用 Word 进行编写，但由于显示排版等问题，本次采用了 Markdown 进行编写，在编写时使用了 Markdown Preview Enhanced 插件。本文介绍 Markdown Preview Enhanced 插件的安装及所使用的功能。

## 安装

打开 vscode 编辑器，打开扩展栏，输入 `Markdown Preview Enhanced` ,第一个就是，点击安装后即可。

## 功能介绍

接下来将介绍一些在编写文档中所使用的功能。

### diagrams

Markdown Preview Enhanced 插件支持 low charts, sequence diagrams, mermaid, PlantUML, WaveDrom, GraphViz，Vega & Vega-lite，Ditaa 图像渲染。

在文档中我使用了 mermaid 和 Vega-lite，Vega-lite 用于绘制图表，mermaid 用于绘制流程图。

接下来介绍 markdown 中如何使用 Vega-lite 绘制图表，使用以下代码即可绘制一个漂亮的饼图：

![alt text](https://jasminides.com/img/markdown-plugin/carbon%20%281%29.png)

![alt text](https://jasminides.com/img/markdown-plugin/Snipaste_2024-08-24_00-33-24.png)

如果想要居中的效果，可以添加 `{align="center"}` 来设置居中的效果。

mermaid 可以用来绘制流程图，使用以下代码即可绘制一个简单的流程图：

![alt text](https://jasminides.com/img/markdown-plugin/carbon%20%283%29.png)

![alt text](https://jasminides.com/img/markdown-plugin/Snipaste_2024-08-24_00-33-32.png)

如果我们想要添加 css 效果该怎么办呢，可以通过 HTML + css 的形式来显示我们想要的效果：

```
a<strong style="color:#F00">上线</strong>
复制
```

![alt text](https://jasminides.com/img/markdown-plugin/Snipaste_2024-08-24_00-34-43.png)

可以看到通过这种方式，我们就可以轻松实现我们想要的效果。

## 小结

Markdown Preview Enhanced 插件功能非常强大，除了文中介绍的功能，还有 幻灯片、自定义 CSS、主题、自定义 markdown parse 等功能，有兴趣的可以自行探索。

## 参考

- [https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)

- [https://github.com/shd101wyy/markdown-preview-enhanced](https://github.com/shd101wyy/markdown-preview-enhanced)

- [https://shd101wyy.github.io/markdown-preview-enhanced/#/zh-cn/](https://shd101wyy.github.io/markdown-preview-enhanced/#/zh-cn/)

- [https://vega.github.io/vega-lite/](https://vega.github.io/vega-lite/)

- [https://github.com/knsv/mermaid](https://github.com/knsv/mermaid)


giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fmarkdown-preview-enhanced%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/markdown-preview-enhanced/#top "Go to Top (Alt + G)")

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

## Markdown Preview Enhanced
前言 最近需要写总结报告，以前写总结报告时，往往使用 Word 进行编写，但由于显示排版等问题，本次采用了 Markdown 进行编写，在编写时使用了 Markdown Preview Enhanced 插件。本文介绍 Markdown Preview Enhanced 插件的安装及所使用的功能。
安装 打开 vscode 编辑器，打开扩展栏，输入 Markdown Preview Enhanced ,第一个就是，点击安装后即可。
功能介绍 接下来将介绍一些在编写文档中所使用的功能。
diagrams Markdown Preview Enhanced 插件支持 low charts, sequence diagrams, mermaid, PlantUML, WaveDrom, GraphViz，Vega & Vega-lite，Ditaa 图像渲染。
在文档中我使用了 mermaid 和 Vega-lite，Vega-lite 用于绘制图表，mermaid 用于绘制流程图。
接下来介绍 markdown 中如何使用 Vega-lite 绘制图表，使用以下代码即可绘制一个漂亮的饼图：
如果想要居中的效果，可以添加 {align="center"}来设置居中的效果。
mermaid 可以用来绘制流程图，使用以下代码即可绘制一个简单的流程图：
如果我们想要添加 css 效果该怎么办呢，可以通过 HTML + css 的形式来显示我们想要的效果：
...

 [post link to Markdown Preview Enhanced plugin introduction and simple use](https://jasminides.com/posts/markdown-preview-enhanced/) [Go to Top (Alt + G)](https://jasminides.com/tags/visualstudio/#top "Go to Top (Alt + G)")

## Go-Humanize Guide
目录

- [前言](https://jasminides.com/posts/go-humanize-introduce-/#%e5%89%8d%e8%a8%80)
- [安装](https://jasminides.com/posts/go-humanize-introduce-/#%e5%ae%89%e8%a3%85)
- [使用](https://jasminides.com/posts/go-humanize-introduce-/#%e4%bd%bf%e7%94%a8)
  - [容量转换](https://jasminides.com/posts/go-humanize-introduce-/#%e5%ae%b9%e9%87%8f%e8%bd%ac%e6%8d%a2)
  - [时间转换](https://jasminides.com/posts/go-humanize-introduce-/#%e6%97%b6%e9%97%b4%e8%bd%ac%e6%8d%a2)
  - [千分位转换](https://jasminides.com/posts/go-humanize-introduce-/#%e5%8d%83%e5%88%86%e4%bd%8d%e8%bd%ac%e6%8d%a2)
  - [位序](https://jasminides.com/posts/go-humanize-introduce-/#%e4%bd%8d%e5%ba%8f)
- [小结](https://jasminides.com/posts/go-humanize-introduce-/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/go-humanize-introduce-/#%e5%8f%82%e8%80%83)

## 前言

今天在 Github 查看一些开源项目时，发现了一个"人性化"的项目 go-humanize，此项目可以将一些常见的容量、时间、千分位转换为人们可以理解的形式，例如一个文件大小是 2000000 bytes，我们不能很好的理解，但如果告诉你是 2mb，我们就能很好的理解了。go-humanize 就是方便的将一些不太能快速理解的数字转换为人们可以理解的形式。

## 安装

使用以下命令安装：

```shell
go get github.com/dustin/go-humanize

```

复制

## 使用

接下来分别介绍一些常见的功能。

### 容量转换

现在我们有一个文件大小是 52854982 bytes，我们使用 humanize 包的 Bytes 方法将其转换为人们可以理解的形式 53MB，也可以使用 IBytes 方法转换为 MIB 单位的值。也可以使用 ParseBytes 方法将可以理解的形式转换为 bytes 单位的值。

```go
	fmt.Printf("That file is %s.\n", humanize.IBytes(52854982))
	fmt.Printf("That file is %s.", humanize.Bytes(52854982))

```

复制

### 时间转换

时间转换与容量转换类型，使用方法十分类似，使用方法如下：

```go
	t := time.Now().Add(time.Hour * -7)
	fmt.Printf("This was touched %s.", humanize.Time(t)) //This was touched 7 hours ago.

```

复制

Time 根据相对时间转换为人们可以理解的形式，例如：xx 天之前、xx 小时之后等形式。

### 千分位转换

如果我们想在数字中添加逗号，就可以使用 Comma 方法，例如在处理金额时，我们通常会使用逗号将数字分隔开，例如 1,000,000,000

```go
    	fmt.Printf("num is %s.", humanize.Comma(1000000000))

```

复制

还可以使用 Commaf 方法将浮点数转换为千分位形式。

### 位序

在日常使用中，我们有时需要表示位序例如 1st、2nd、3rd、4th 等，humanize 包也提供了相应的功能。

```go
    fmt.Printf("num is %s.", humanize.Ordinal(1000000000))

```

复制

简单看了下源码，发现函数十分简单：

```go
func Ordinal(x int) string {
	suffix := "th"
	switch x % 10 {
	case 1:
		if x%100 != 11 {
			suffix = "st"
		}
	case 2:
		if x%100 != 12 {
			suffix = "nd"
		}
	case 3:
		if x%100 != 13 {
			suffix = "rd"
		}
	}
	return strconv.Itoa(x) + suffix
}

```

复制

## 小结

本文介绍了 go-humanize 包的一些使用方法，可以方便的将一些数字转换为人们可以理解的形式。go-humanize 还有一些格式化的函数，感兴趣的读者可以自行查看源码。

## 参考

- [https://groups.google.com/g/golang-nuts/c/l8NhI74jl-4](https://groups.google.com/g/golang-nuts/c/l8NhI74jl-4)
- [https://github.com/dustin/go-humanize](https://github.com/dustin/go-humanize)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fgo-humanize-introduce-%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/go-humanize-introduce-/#top "Go to Top (Alt + G)")

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

## Using go-humanize Library
前言 今天在 Github 查看一些开源项目时，发现了一个"人性化"的项目 go-humanize，此项目可以将一些常见的容量、时间、千分位转换为人们可以理解的形式，例如一个文件大小是 2000000 bytes，我们不能很好的理解，但如果告诉你是 2mb，我们就能很好的理解了。go-humanize 就是方便的将一些不太能快速理解的数字转换为人们可以理解的形式。
安装 使用以下命令安装：
go get github.com/dustin/go-humanize 使用 接下来分别介绍一些常见的功能。
容量转换 现在我们有一个文件大小是 52854982 bytes，我们使用 humanize 包的 Bytes 方法将其转换为人们可以理解的形式 53MB，也可以使用 IBytes 方法转换为 MIB 单位的值。也可以使用 ParseBytes 方法将可以理解的形式转换为 bytes 单位的值。
fmt.Printf("That file is %s.\\n", humanize.IBytes(52854982)) fmt.Printf("That file is %s.", humanize.Bytes(52854982)) 时间转换 时间转换与容量转换类型，使用方法十分类似，使用方法如下：
t := time.Now().Add(time.Hour \* -7) fmt.Printf("This was touched %s.", humanize.Time(t)) //This was touched 7 hours ago. Time 根据相对时间转换为人们可以理解的形式，例如：xx 天之前、xx 小时之后等形式。
千分位转换 如果我们想在数字中添加逗号，就可以使用 Comma 方法，例如在处理金额时，我们通常会使用逗号将数字分隔开，例如 1,000,000,000
fmt.Printf("num is %s.", humanize.Comma(1000000000)) 还可以使用 Commaf 方法将浮点数转换为千分位形式。
位序 在日常使用中，我们有时需要表示位序例如 1st、2nd、3rd、4th 等，humanize 包也提供了相应的功能。
...

 [post link to go humanize 介绍](https://jasminides.com/posts/go-humanize-introduce-/) [Go to Top (Alt + G)](https://jasminides.com/tags/humanize/#top "Go to Top (Alt + G)")

## WSL Proxy Configuration
前言 最近在使用 WSL 时，想要在 WSL 中使用代理，但由于一些历史原因，宿主机开启的代理，WSL 无法使用，为了解决这个问题，查找了相关文档，在本文记录一下。
解决 在 windows C:\\Users<your\_username> 目录下创建 .wslconfig 文件，输入以下内容：
\[experimental\] autoMemoryReclaim=gradual networkingMode=mirrored dnsTunneling=true firewall=true autoProxy=true 然后重启 WSL: wsl --shutdown
networkingMode 为 mirrored 表示网络模式使用镜像模式，会镜像宿主机的网络设置，能更好的集成宿主机和 WSL 的网络。
autoProxy 开启了自动代理的功能，意味 WSL 自动配置代理设置。
参考 https://github.com/microsoft/WSL/issues/10753 https://learn.microsoft.com/en-us/windows/wsl/wsl-config#experimental-settings

 [post link to 解决检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。](https://jasminides.com/posts/wsl_error1/) [Go to Top (Alt + G)](https://jasminides.com/tags/wsl/#top "Go to Top (Alt + G)")

## WSL Proxy Configuration
目录

- [前言](https://jasminides.com/posts/wsl_error1/#%e5%89%8d%e8%a8%80)
- [解决](https://jasminides.com/posts/wsl_error1/#%e8%a7%a3%e5%86%b3)
- [参考](https://jasminides.com/posts/wsl_error1/#%e5%8f%82%e8%80%83)

## 前言

最近在使用 WSL 时，想要在 WSL 中使用代理，但由于一些历史原因，宿主机开启的代理，WSL 无法使用，为了解决这个问题，查找了相关文档，在本文记录一下。

## 解决

在 windows C:\\Users<your\_username> 目录下创建 .wslconfig 文件，输入以下内容：

```text
[experimental]
autoMemoryReclaim=gradual
networkingMode=mirrored
dnsTunneling=true
firewall=true
autoProxy=true

```

复制

然后重启 WSL: `wsl --shutdown`

networkingMode 为 mirrored 表示网络模式使用镜像模式，会镜像宿主机的网络设置，能更好的集成宿主机和 WSL 的网络。

autoProxy 开启了自动代理的功能，意味 WSL 自动配置代理设置。

## 参考

- [https://github.com/microsoft/WSL/issues/10753](https://github.com/microsoft/WSL/issues/10753)
- [https://learn.microsoft.com/en-us/windows/wsl/wsl-config#experimental-settings](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#experimental-settings)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fwsl_error1%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/wsl_error1/#top "Go to Top (Alt + G)")

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

## AI Programming Assistant
目录

- [介绍](https://jasminides.com/posts/cody/#%e4%bb%8b%e7%bb%8d)
- [价格](https://jasminides.com/posts/cody/#%e4%bb%b7%e6%a0%bc)
- [安装](https://jasminides.com/posts/cody/#%e5%ae%89%e8%a3%85)
- [使用](https://jasminides.com/posts/cody/#%e4%bd%bf%e7%94%a8)
  - [代码补全](https://jasminides.com/posts/cody/#%e4%bb%a3%e7%a0%81%e8%a1%a5%e5%85%a8)
  - [聊天](https://jasminides.com/posts/cody/#%e8%81%8a%e5%a4%a9)
  - [命令](https://jasminides.com/posts/cody/#%e5%91%bd%e4%bb%a4)
  - [OpenCtx](https://jasminides.com/posts/cody/#openctx)
- [小结](https://jasminides.com/posts/cody/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/cody/#%e5%8f%82%e8%80%83)

## 介绍

cody 是一个 AI 编程助手，可以帮助你更快更好的理解代码，编写代码，解决代码中的问题。通过本地代码仓库和远程代码库提取上下文，让你能够更好的理解和编写代码。Cody 目前可以在以下编程工具中使用:

> 1. VS Code
> 2. JetBrains IDE
> 3. Neovim (实验性)
> 4. Web (实验性)

Cody 主要有以下功能:

> - 自动完成 基于代码上下文的自动补全
> - 聊天 在聊天视图中询问代码相关的问题
> - 命令 为常见的操作提供了快捷命令，例如：生成文档，添加测试，检测代码问题
> - 调试 在编辑器中调试代码，帮你寻找代码中的问题
> - 忽略 可以过滤某些文件及过滤某些仓库

## 价格

介绍完 Cody 的特点后，接下来介绍大家关心的价格问题，Cody 有 3 个版本，分别是 Free、Pro、Enterprise.

Free 版本为免费版，目前每月提供 20 次聊天次数、500 次代码自动完成，今天查看 sourcegraph 的 blog，发现 Free 版本的额度提高了，代码自动完成次数为无限次，聊天和命令次数增加了 10 倍为 200 次。

Pro 版本为每个月 9 美元，提供了不限次数的代码补全及聊天功能及提供了 GPT-4o 等高级 LLM.

Enterprise 的价格需要联系 sourcegraph 的销售人员，Enterprise 相较于 Pro 版提供了更多的团队功能。

## 安装

接下来介绍如何安装 Cody，主要介绍 VS Code 中如何安装：

1 打开 VS Code

2 打开扩展界面，搜索 Cody AI，点击安装

3 安装完可能需要重启 VS Code

4 安装完，Cody 就会在活动栏中显示

![alt text](https://jasminides.com/img/cody/image.png)

## 使用

接下来介绍 Cody 的主要功能

### 代码补全

代码补全是基础功能，Cody 使用了 StarCoder 模型，可以很好的帮助代码的补全，只要输入部分代码或注释，就会出现相应的提示代码。

![alt text](https://jasminides.com/img/cody/image-2.png)

### 聊天

打开一个代码仓库，这里打开 gaby 仓库，gaby 是 Go 官方团队的新型使用了 AI 技术的 Github bot, 新建一个 Chat 窗口，询问 gaby 仓库的相关信息，可以看到很好的回答了项目的每个文件夹的功能。

![alt text](https://jasminides.com/img/cody/image-1.png)

![alt text](https://jasminides.com/img/cody/image-3.png)

在聊天中，Cody 也可以针对问题生成代码，你可以选择相应的代码插入原有的代码中。

### 命令

在 Cody 菜单中有一个独立的命令面板，里面提供了常见的聊天，编辑代码，解释代码等功能，可以方便的使用。还可以通过自定义命令功能创建重复使用的提示词，以适应相应的开发流程。

### OpenCtx

通过 OpenCtx，用户提供相关的上下文信息，可以更好的理解代码。

解释代码，编写代码单元测试这些功能就不一一介绍了，都是编程助手中常用的功能。

## 小结

本文简单的介绍了 Cody 的功能，通过 Cody 可以更好的理解代码，编写代码，解决代码中的问题。

相较于作者使用过的其它编程助手，Cody 提供的 LLM 更多，并且能更好的通过代码仓库上下文理解代码。

## 参考

- [https://sourcegraph.com/docs/cody](https://sourcegraph.com/docs/cody)
- [https://sourcegraph.com/blog/making-cody-free-10x-better](https://sourcegraph.com/blog/making-cody-free-10x-better)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fcody%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/cody/#top "Go to Top (Alt + G)")

## AI 编程助手 Cody
介绍 cody 是一个 AI 编程助手，可以帮助你更快更好的理解代码，编写代码，解决代码中的问题。通过本地代码仓库和远程代码库提取上下文，让你能够更好的理解和编写代码。Cody 目前可以在以下编程工具中使用:
VS Code JetBrains IDE Neovim (实验性) Web (实验性) Cody 主要有以下功能:
自动完成 基于代码上下文的自动补全 聊天 在聊天视图中询问代码相关的问题 命令 为常见的操作提供了快捷命令，例如：生成文档，添加测试，检测代码问题 调试 在编辑器中调试代码，帮你寻找代码中的问题 忽略 可以过滤某些文件及过滤某些仓库 价格 介绍完 Cody 的特点后，接下来介绍大家关心的价格问题，Cody 有 3 个版本，分别是 Free、Pro、Enterprise.
Free 版本为免费版，目前每月提供 20 次聊天次数、500 次代码自动完成，今天查看 sourcegraph 的 blog，发现 Free 版本的额度提高了，代码自动完成次数为无限次，聊天和命令次数增加了 10 倍为 200 次。
Pro 版本为每个月 9 美元，提供了不限次数的代码补全及聊天功能及提供了 GPT-4o 等高级 LLM.
Enterprise 的价格需要联系 sourcegraph 的销售人员，Enterprise 相较于 Pro 版提供了更多的团队功能。
安装 接下来介绍如何安装 Cody，主要介绍 VS Code 中如何安装：
...

 [post link to AI 编程助手 - Cody](https://jasminides.com/posts/cody/) [Go to Top (Alt + G)](https://jasminides.com/tags/cody/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fcody%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801881061&bpp=2&bdt=178&idt=57&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=4852083333112&rume=1&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C42531705%2C95353451%2C31091145%2C95355301%2C31061691%2C31061692&oid=2&pvsid=2677230457767332&tmod=1001552682&uas=0&nvt=1&fsapi=1&fc=1920&brdim=520%2C520%2C520%2C520%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=74)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Powerful Web Crawler
katana 介绍 katana 是一款强大的新一代的网络爬虫工具，通过使用 katana，用户能够快速的进行互联网资源的爬取和渗透测试阶段的收集任务。
特点 katana 有以下特点：
快速及高可配置的网络爬虫 标准及无头模式 主动和被动模式 JavaScript 脚本爬取解析 定制的表单内容自动填充 爬取范围控制 可自定义设置输出字段 输入数据 支持标准输入 (STDIN)，URL 和列表 (LIST) 输出数据 支持 STDOUT、文件和 JSON 格式 安装 接下来介绍如何安装 katana
katana 的安装需要 go1.18 版本以上，可以执行以下命令或下载 Github 仓库的发布版本。
go install github.com/projectdiscovery/katana/cmd/katana@latest windows 在安装中可能会遇到以下报错：
github.com/smacker/go-tree-sitter/javascript: build constraints exclude all Go files in C:\\Users\\overstarry\\go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\javascript # github.com/smacker/go-tree-sitter go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:17:18: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:21:21: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:25:20: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:30:26: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:34:20: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:38:32: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:43:9: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:46:18: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:68:40: undefined: Node 可以使用以下命令解决：
...

 [post link to katana 新一代的爬虫工具](https://jasminides.com/posts/katana/) [Go to Top (Alt + G)](https://jasminides.com/tags/crawler/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fcrawler%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801881263&bpp=3&bdt=276&idt=141&shv=r20250319&mjsv=m202503190101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=7426911757115&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C31084127%2C31091146%2C95355965&oid=2&pvsid=2971785443329037&tmod=247707018&uas=0&nvt=1&fsapi=1&fc=1920&brdim=130%2C130%2C130%2C130%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=166)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Katana Web Crawler
katana 介绍 katana 是一款强大的新一代的网络爬虫工具，通过使用 katana，用户能够快速的进行互联网资源的爬取和渗透测试阶段的收集任务。
特点 katana 有以下特点：
快速及高可配置的网络爬虫 标准及无头模式 主动和被动模式 JavaScript 脚本爬取解析 定制的表单内容自动填充 爬取范围控制 可自定义设置输出字段 输入数据 支持标准输入 (STDIN)，URL 和列表 (LIST) 输出数据 支持 STDOUT、文件和 JSON 格式 安装 接下来介绍如何安装 katana
katana 的安装需要 go1.18 版本以上，可以执行以下命令或下载 Github 仓库的发布版本。
go install github.com/projectdiscovery/katana/cmd/katana@latest windows 在安装中可能会遇到以下报错：
github.com/smacker/go-tree-sitter/javascript: build constraints exclude all Go files in C:\\Users\\overstarry\\go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\javascript # github.com/smacker/go-tree-sitter go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:17:18: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:21:21: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:25:20: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:30:26: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:34:20: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:38:32: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:43:9: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:46:18: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:68:40: undefined: Node 可以使用以下命令解决：
...

 [post link to katana 新一代的爬虫工具](https://jasminides.com/posts/katana/) [Go to Top (Alt + G)](https://jasminides.com/tags/katana/#top "Go to Top (Alt + G)")

## Katana Web Crawler
目录

- [katana 介绍](https://jasminides.com/posts/katana/#katana-%e4%bb%8b%e7%bb%8d)
  - [特点](https://jasminides.com/posts/katana/#%e7%89%b9%e7%82%b9)
- [安装](https://jasminides.com/posts/katana/#%e5%ae%89%e8%a3%85)
  - [Docker 安装](https://jasminides.com/posts/katana/#docker-%e5%ae%89%e8%a3%85)
- [使用](https://jasminides.com/posts/katana/#%e4%bd%bf%e7%94%a8)
  - [爬取多个 url](https://jasminides.com/posts/katana/#%e7%88%ac%e5%8f%96%e5%a4%9a%e4%b8%aa-url)
  - [爬取模式](https://jasminides.com/posts/katana/#%e7%88%ac%e5%8f%96%e6%a8%a1%e5%bc%8f)
  - [爬取范围](https://jasminides.com/posts/katana/#%e7%88%ac%e5%8f%96%e8%8c%83%e5%9b%b4)
    - [-field-scope](https://jasminides.com/posts/katana/#-field-scope)
    - [-crawl-scope](https://jasminides.com/posts/katana/#-crawl-scope)
    - [-crawl-out-scope](https://jasminides.com/posts/katana/#-crawl-out-scope)
  - [其它](https://jasminides.com/posts/katana/#%e5%85%b6%e5%ae%83)
  - [katana 库](https://jasminides.com/posts/katana/#katana-%e5%ba%93)
- [参考](https://jasminides.com/posts/katana/#%e5%8f%82%e8%80%83)

## katana 介绍

katana 是一款强大的新一代的网络爬虫工具，通过使用 katana，用户能够快速的进行互联网资源的爬取和渗透测试阶段的收集任务。

### 特点

katana 有以下特点：

- 快速及高可配置的网络爬虫
- 标准及无头模式
- 主动和被动模式
- JavaScript 脚本爬取解析
- 定制的表单内容自动填充
- 爬取范围控制
- 可自定义设置输出字段
- 输入数据 支持标准输入 (STDIN)，URL 和列表 (LIST)
- 输出数据 支持 STDOUT、文件和 JSON 格式

## 安装

接下来介绍如何安装 katana

katana 的安装需要 go1.18 版本以上，可以执行以下命令或下载 Github 仓库的发布版本。

```shell
go install github.com/projectdiscovery/katana/cmd/katana@latest

```

复制

windows 在安装中可能会遇到以下报错：

```text
github.com/smacker/go-tree-sitter/javascript: build constraints exclude all Go files in C:\Users\overstarry\go\pkg\mod\github.com\smacker\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\javascript
# github.com/smacker/go-tree-sitter
go\pkg\mod\github.com\smacker\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\iter.go:17:18: undefined: Node
go\pkg\mod\github.com\smacker\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\iter.go:21:21: undefined: Node
go\pkg\mod\github.com\smacker\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\iter.go:25:20: undefined: Node
go\pkg\mod\github.com\smacker\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\iter.go:30:26: undefined: Node
go\pkg\mod\github.com\smacker\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\iter.go:34:20: undefined: Node
go\pkg\mod\github.com\smacker\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\iter.go:38:32: undefined: Node
go\pkg\mod\github.com\smacker\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\iter.go:43:9: undefined: Node
go\pkg\mod\github.com\smacker\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\iter.go:46:18: undefined: Node
go\pkg\mod\github.com\smacker\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\iter.go:68:40: undefined: Node

```

复制

可以使用以下命令解决：

```shell
choco install zig
set CGO_ENABLED=1&set GOOS=windows&set GOARCH=amd64&set CC=zig cc&set CXX=zig c++
go install github.com/projectdiscovery/katana/cmd/katana@latest

```

复制

### Docker 安装

katana 还支持 Docker 进行使用，执行以下命令：

```shell
docker pull projectdiscovery/katana:latest
docker run projectdiscovery/katana:latest -u https://tesla.com

```

复制

## 使用

接下来的使用环境会以 Docker 环境为主。

### 爬取多个 url

使用 -u 参数，可以爬取指定网站的数据，可以看到 overstarry.vip 的网站链接都显示了。

`docker run projectdiscovery/katana:latest -u https://overstarry.vip`

![alt text](https://jasminides.com/img/katana/image.png)

如果想要一次获取多个网站的数据，直接添加多个 URL 即可，多个 URL 之间以逗号分隔。

需要注意的是，爬取 url 时，会将当前 url 上的所有链接都会获取下来，包括超链接。

### 爬取模式

1 标准

标准模式使用 go 原生 http 进行数据采集，采集速度会更快，但不会处理 Javascript 和 Dom 渲染，不适合用于一些有复杂动态渲染的网站，

2 无头浏览器模式

无头模式使用无头浏览器，在浏览器上下文进行数据的获取，有以下优点:

1. Http 指纹合法
2. 可以处理更复杂的一些网站

### 爬取范围

如果没有限定爬取范围，katana 爬取可能会是无止境的，所有一般需要限定爬取的数据范围。

#### -field-scope

有三个选项:

```
* rdn 爬取根域名及所有子域名 (默认)
* fqdn 限定爬取的子域名
* dn 爬取的范围为指定关键字域名
复制
```

#### -crawl-scope

#### -crawl-out-scope

定义不爬取的内容范围，支持正则表达式

### 其它

除了这些参数，katana 还支持很多其它参数，感兴趣的读者可以自行研究

### katana 库

除了 cli 使用外，katana 还支持在代码中进行使用。

## 参考

- [https://github.com/projectdiscovery/katana](https://github.com/projectdiscovery/katana)
- [https://github.com/projectdiscovery/katana/issues/866](https://github.com/projectdiscovery/katana/issues/866)
- [https://github.com/projectdiscovery/katana/issues/624#issuecomment-1764007669](https://github.com/projectdiscovery/katana/issues/624#issuecomment-1764007669)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fkatana%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/katana/#top "Go to Top (Alt + G)")

## Powerful Web Crawler
katana 介绍 katana 是一款强大的新一代的网络爬虫工具，通过使用 katana，用户能够快速的进行互联网资源的爬取和渗透测试阶段的收集任务。
特点 katana 有以下特点：
快速及高可配置的网络爬虫 标准及无头模式 主动和被动模式 JavaScript 脚本爬取解析 定制的表单内容自动填充 爬取范围控制 可自定义设置输出字段 输入数据 支持标准输入 (STDIN)，URL 和列表 (LIST) 输出数据 支持 STDOUT、文件和 JSON 格式 安装 接下来介绍如何安装 katana
katana 的安装需要 go1.18 版本以上，可以执行以下命令或下载 Github 仓库的发布版本。
go install github.com/projectdiscovery/katana/cmd/katana@latest windows 在安装中可能会遇到以下报错：
github.com/smacker/go-tree-sitter/javascript: build constraints exclude all Go files in C:\\Users\\overstarry\\go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\javascript # github.com/smacker/go-tree-sitter go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:17:18: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:21:21: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:25:20: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:30:26: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:34:20: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:38:32: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:43:9: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:46:18: undefined: Node go\\pkg\\mod\\github.com\\smacker\\go-tree-sitter@v0.0.0-20230720070738-0d0a9f78d8f8\\iter.go:68:40: undefined: Node 可以使用以下命令解决：
...

 [post link to katana 新一代的爬虫工具](https://jasminides.com/posts/katana/) [Go to Top (Alt + G)](https://jasminides.com/tags/spider/#top "Go to Top (Alt + G)")

## Website Monitoring Tools
介绍 Tianji 是一个集网站分析、网站状态监控、服务状态监控集一体的工具平台。
在我们日常使用中，我们在观察监控一个网站使往往需要使用多个工具一起使用，例如使用 GA 来进行 PV/UV 数据的收集，使用 uptime monitor 来查看服务器的网络及连通性，使用 prometheus 来查看服务器的状态等 那么有没有一个工具能满足这些需求呢？Tianji 就是这样一个工具，能够更方便更简洁的满足用户的需求。
安装 docker 安装 Tianji wget https://raw.githubusercontent.com/msgbyte/tianji/master/docker-compose.yml docker compose up -d 默认账号密码是 admin/admin
kubernetes 安装 Tianji kubernetes 环境下可以使用 Helm 安装
helm repo add msgbyte https://msgbyte.github.io/charts helm search repo tianji helm install tianji msgbyte/tianji 本文使用了 Docker 进行安装，接下来的介绍也会以这个环境为主。
使用 安装完浏览器打开 http://localhost:12345/ 输入默认账号密码即进入主界面。
可以看到有六个栏目，接下来依次介绍这六个栏目的使用。
网站 网站顾名思义就是统计网站的 PV/UV 数据，创建好一个网站后，可以在你的网站中嵌入相应的脚本代码，就可追踪相应的用户数据。
监控器 监控器就是针对网站云服务进行一个相应的监控，保证服务的稳定性。
...

 [post link to Tianji 介绍](https://jasminides.com/posts/tianji/)

起因 最近一个部署了 go 应用的服务器出现了 OOM 的现象，内存占用过高。
原因 通过 Pyroscope 分析得出是因为 Minio 的 go sdk 中的 PutObject 函数占用了大量的内存。Pyroscope 是什么，前面的文章已经介绍过了，这里就不过多介绍了。
接下来我们通过查看相关的源码来查看是什么原因。
// PutObject creates an object in a bucket. // // You must have WRITE permissions on a bucket to create an object. // // - For size smaller than 16MiB PutObject automatically does a // single atomic PUT operation. // // - For size larger than 16MiB PutObject automatically does a // multipart upload operation. // // - For size input as -1 PutObject does a multipart Put operation // until input stream reaches EOF. Maximum object size that can // be uploaded through this operation will be 5TiB. // // WARNING: Passing down '-1' will use memory and these cannot // be reused for best outcomes for PutObject(), pass the size always. // // NOTE: Upon errors during upload multipart operation is entirely aborted. func (c \*Client) PutObject(ctx context.Context, bucketName, objectName string, reader io.Reader, objectSize int64, opts PutObjectOptions, ) (info UploadInfo, err error) { if objectSize < 0 && opts.DisableMultipart { return UploadInfo{}, errors.New("object size must be provided with disable multipart upload") } err = opts.validate() if err != nil { return UploadInfo{}, err } return c.putObjectCommon(ctx, bucketName, objectName, reader, objectSize, opts) } 从方法的注释可以看出，当传递的大小为 -1 时，会进行多次 put 操作，直到输入流结束。多次 put 操作的最大大小为 5TiB，并且不能重用内存，导致占用大量内存。
...

 [post link to 应用内存升高原因排查](https://jasminides.com/posts/%E5%BA%94%E7%94%A8%E5%86%85%E5%AD%98%E5%8D%87%E9%AB%98%E5%8E%9F%E5%9B%A0%E6%8E%92%E6%9F%A5/)

什么是 Pyroscope? Pyroscope 是一个开源的持续分析系统，使用 Go 语言实现。服务端使用 web 页面查看，提供丰富的分析的功能，客户端提供 Go、Java、Python、Ruby、PHP、.NET 等多种语言的支持，并且支持 PUSH、PULL 两种采集方式。
Pyroscope 是一个开源的持续性能剖析平台。它能够帮你：
找出源代码中的性能问题和瓶颈 解决 CPU 利用率高的问题 理解应用程序的调用树（call tree） 追踪随一段时间内变化的情况 特性：
可以存储来自多个应用程序的多年剖析数据 你可以一次查看多年的数据或单独查看特定的事件 较低的 CPU 开销 数据压缩效率高，磁盘空间要求低 快捷的 UI 界面 部署架构图：
Pyroscope server 安装 Pyroscope server 端可以通过 docker 安装：
docker run -it -p 4040:4040 pyroscope/pyroscope:latest server
也可以在各中操作系统中直接安装。
比如 Mac:
brew install pyroscope-io/brew/pyroscope brew services start pyroscope-server 各 Liunx 发行版也方便安装
比如 ubuntu:
wget https://dl.pyroscope.io/release/pyroscope\_0.10.2\_amd64.deb sudo apt-get install ./pyroscope\_0.10.2\_amd64.deb 安装完成后，就可以通过 web 界面访问了：http://localhost:4040, 你可以通过配置文件更改监听端口以及其它一些配置项。
...

 [post link to Pyroscope 持续分析平台](https://jasminides.com/posts/pyroscope-%E6%8C%81%E7%BB%AD%E5%88%86%E5%B9%B3%E5%8F%B0/) [Go to Top (Alt + G)](https://jasminides.com/tags/monitor/#top "Go to Top (Alt + G)")

## Website Monitoring Tool
介绍 Tianji 是一个集网站分析、网站状态监控、服务状态监控集一体的工具平台。
在我们日常使用中，我们在观察监控一个网站使往往需要使用多个工具一起使用，例如使用 GA 来进行 PV/UV 数据的收集，使用 uptime monitor 来查看服务器的网络及连通性，使用 prometheus 来查看服务器的状态等 那么有没有一个工具能满足这些需求呢？Tianji 就是这样一个工具，能够更方便更简洁的满足用户的需求。
安装 docker 安装 Tianji wget https://raw.githubusercontent.com/msgbyte/tianji/master/docker-compose.yml docker compose up -d 默认账号密码是 admin/admin
kubernetes 安装 Tianji kubernetes 环境下可以使用 Helm 安装
helm repo add msgbyte https://msgbyte.github.io/charts helm search repo tianji helm install tianji msgbyte/tianji 本文使用了 Docker 进行安装，接下来的介绍也会以这个环境为主。
使用 安装完浏览器打开 http://localhost:12345/ 输入默认账号密码即进入主界面。
可以看到有六个栏目，接下来依次介绍这六个栏目的使用。
网站 网站顾名思义就是统计网站的 PV/UV 数据，创建好一个网站后，可以在你的网站中嵌入相应的脚本代码，就可追踪相应的用户数据。
监控器 监控器就是针对网站云服务进行一个相应的监控，保证服务的稳定性。
...

 [post link to Tianji 介绍](https://jasminides.com/posts/tianji/) [Go to Top (Alt + G)](https://jasminides.com/tags/tianji/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Ftianji%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801881185&bpp=3&bdt=281&idt=85&shv=r20250319&mjsv=m202503200101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=6008163356483&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95355339%2C42531706%2C95332928%2C31091179&oid=2&pvsid=1721464237264650&tmod=14448454&uas=0&nvt=1&fsapi=1&fc=1920&brdim=450%2C450%2C450%2C450%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=106)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Website Monitoring Tool
目录

- [介绍](https://jasminides.com/posts/tianji/#%e4%bb%8b%e7%bb%8d)
- [安装](https://jasminides.com/posts/tianji/#%e5%ae%89%e8%a3%85)
  - [docker 安装 Tianji](https://jasminides.com/posts/tianji/#docker-%e5%ae%89%e8%a3%85-tianji)
  - [kubernetes 安装 Tianji](https://jasminides.com/posts/tianji/#kubernetes-%e5%ae%89%e8%a3%85-tianji)
- [使用](https://jasminides.com/posts/tianji/#%e4%bd%bf%e7%94%a8)
  - [网站](https://jasminides.com/posts/tianji/#%e7%bd%91%e7%ab%99)
  - [监控器](https://jasminides.com/posts/tianji/#%e7%9b%91%e6%8e%a7%e5%99%a8)
  - [服务器](https://jasminides.com/posts/tianji/#%e6%9c%8d%e5%8a%a1%e5%99%a8)
  - [遥测](https://jasminides.com/posts/tianji/#%e9%81%a5%e6%b5%8b)
  - [页面](https://jasminides.com/posts/tianji/#%e9%a1%b5%e9%9d%a2)
- [小结](https://jasminides.com/posts/tianji/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/tianji/#%e5%8f%82%e8%80%83)

## 介绍

Tianji 是一个集网站分析、网站状态监控、服务状态监控集一体的工具平台。

在我们日常使用中，我们在观察监控一个网站使往往需要使用多个工具一起使用，例如使用 GA 来进行 PV/UV 数据的收集，使用 uptime monitor 来查看服务器的网络及连通性，使用 prometheus 来查看服务器的状态等 那么有没有一个工具能满足这些需求呢？Tianji 就是这样一个工具，能够更方便更简洁的满足用户的需求。

## 安装

### docker 安装 Tianji

```shell
wget https://raw.githubusercontent.com/msgbyte/tianji/master/docker-compose.yml
docker compose up -d

```

复制

默认账号密码是 admin/admin

### kubernetes 安装 Tianji

kubernetes 环境下可以使用 Helm 安装

```shell
helm repo add msgbyte https://msgbyte.github.io/charts
helm search repo tianji
helm install tianji msgbyte/tianji

```

复制

本文使用了 Docker 进行安装，接下来的介绍也会以这个环境为主。

## 使用

安装完浏览器打开 http://localhost:12345/ 输入默认账号密码即进入主界面。

![alt text](https://jasminides.com/img/tianji/image.png)

可以看到有六个栏目，接下来依次介绍这六个栏目的使用。

### 网站

网站顾名思义就是统计网站的 PV/UV 数据，创建好一个网站后，可以在你的网站中嵌入相应的脚本代码，就可追踪相应的用户数据。

![alt text](https://jasminides.com/img/tianji/image-1.png)

### 监控器

监控器就是针对网站云服务进行一个相应的监控，保证服务的稳定性。

![alt text](https://jasminides.com/img/tianji/image-2.png)

![alt text](https://jasminides.com/img/tianji/image-4.png)

与传统的监控服务相比，Tianji 支持通过自定义脚本的方式来支持更多的定制化的场景，具体的可以查看相应的文档。

### 服务器

服务器就是在服务器上安装相应的 agent 服务来接收相应的服务器 CPU 等数据。

![alt text](https://jasminides.com/img/tianji/image-5.png)

### 遥测

遥测是一种常见的技术，它涉及最少和匿名的信息报告，以解决隐私问题，同时仍满足内容创建者的基本分析需求。通过创建一个 1px 大小的空白透明像素图像，我们可以收集我们无法控制的网站上的访问者数据。

![alt text](https://jasminides.com/img/tianji/image-7.png)

### 页面

就是通过一个页面来展示创建的监控器。通过创建页面，你可以通过一个域名来对外展示服务器的健康状态。

![alt text](https://jasminides.com/img/tianji/image-6.png)

## 小结

本文介绍了一个集健康遥测服务器状态监控等的工具 Tianji，介绍了 Tianji 的安装及简单使用。

## 参考

- [https://tianji.msgbyte.com/](https://tianji.msgbyte.com/)
- [https://github.com/msgbyte/tianji](https://github.com/msgbyte/tianji)
- [https://tianji.msgbyte.com/docs/monitor/custom-script](https://tianji.msgbyte.com/docs/monitor/custom-script)
- [https://juejin.cn/post/7344970197130346535?searchId=202406221440178AD4D52AAE13871164DA](https://juejin.cn/post/7344970197130346535?searchId=202406221440178AD4D52AAE13871164DA)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Ftianji%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/tianji/#top "Go to Top (Alt + G)")

## AI File Type Detection
目录

- [magika 介绍](https://jasminides.com/posts/magika/#magika-%e4%bb%8b%e7%bb%8d)
- [安装](https://jasminides.com/posts/magika/#%e5%ae%89%e8%a3%85)
- [运行](https://jasminides.com/posts/magika/#%e8%bf%90%e8%a1%8c)
- [小结](https://jasminides.com/posts/magika/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/magika/#%e5%8f%82%e8%80%83)

## magika 介绍

Magika 是 Google 推出的一个新型工具，使用 AI 用来文件类型的检测，采用了高度优化的 Keras 模型，具有较高的准确性、模型较小等优点，支持 [100](https://github.com/google/magika/blob/main/docs/supported_content_types_list.md) 多种文件类型，准确性高达 99%,推测每个文件的时间大约 5 ms。

Magika 在 Google 内部已被大量使用，用于 Gmail，网络硬盘等应用，检测各种文件，提高了用户的安全性。

Magika 提供了 Pyhton 命令行、Pyhton API 和 js 包等多种方式使用，还支持批量处理提高推理速度。

## 安装

可以使用 pip 命令进行安装： `pip install magika`

如果没有 Python 环境，还可以 Docker 中进行使用：

```
git clone https://github.com/google/magika
cd magika/
docker build -t magika .
docker run -it --rm -v $(pwd):/magika magika -r /magika/tests_data
复制
```

如果 Docker 环境也没有，那你可以使用 Google 部署的网站进行试用 [https://google.github.io/magika/](https://google.github.io/magika/)。

## 运行

运行仓库提供的测试数据 ( `magika -r /magika/tests_data`):
![alt text](https://jasminides.com/img/magika/image.png)

可以看到文件的类型很精准的被识别出来了。

接下来做个试验，将一个 png 的图片的后缀修改为 jpg ,看看还能否正确识别，可以看到还是成功精准识别了。

![alt text](https://jasminides.com/img/magika/image-1.png)

## 小结

本文介绍了一种使用 AI 进行文件类型检测的工具 magika，相较于其它类型检测工具，magika 依托于数据集和模型的精度，可以大大提高识别文件类型的精度和速度。

## 参考

- [https://opensource.googleblog.com/2024/02/magika-ai-powered-fast-and-efficient-file-type-identification.html](https://opensource.googleblog.com/2024/02/magika-ai-powered-fast-and-efficient-file-type-identification.html)
- [https://github.com/google/magika](https://github.com/google/magika)
- [https://github.com/google/magika/blob/main/js/README.md](https://github.com/google/magika/blob/main/js/README.md)
- [https://github.com/google/magika/blob/main/docs/command\_line\_interface.md](https://github.com/google/magika/blob/main/docs/command_line_interface.md)
- [https://google.github.io/magika/](https://google.github.io/magika/)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fmagika%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/magika/#top "Go to Top (Alt + G)")

## AI File Type Detection
magika 介绍 Magika 是 Google 推出的一个新型工具，使用 AI 用来文件类型的检测，采用了高度优化的 Keras 模型，具有较高的准确性、模型较小等优点，支持100多种文件类型，准确性高达 99%,推测每个文件的时间大约 5 ms。
Magika 在 Google 内部已被大量使用，用于 Gmail，网络硬盘等应用，检测各种文件，提高了用户的安全性。
Magika 提供了 Pyhton 命令行、Pyhton API 和 js 包等多种方式使用，还支持批量处理提高推理速度。
安装 可以使用 pip 命令进行安装：pip install magika
如果没有 Python 环境，还可以 Docker 中进行使用：
git clone https://github.com/google/magika cd magika/ docker build -t magika . docker run -it --rm -v $(pwd):/magika magika -r /magika/tests\_data 如果 Docker 环境也没有，那你可以使用 Google 部署的网站进行试用 https://google.github.io/magika/。
运行 运行仓库提供的测试数据 (magika -r /magika/tests\_data): 可以看到文件的类型很精准的被识别出来了。
接下来做个试验，将一个 png 的图片的后缀修改为 jpg ,看看还能否正确识别，可以看到还是成功精准识别了。
...

 [post link to AI 检测文件类型 Magika](https://jasminides.com/posts/magika/) [Go to Top (Alt + G)](https://jasminides.com/tags/magika/#top "Go to Top (Alt + G)")

## AI Bot Development
前言 Coze 是新一代一站式 AI Bot 开发平台。无论你是否有编程基础，都可以在 Coze 平台上快速搭建基于 AI 模型的各类问答 Bot，从解决简单的问答到处理复杂逻辑的对话。并且，你可以将搭建的 Bot 发布到各类社交平台和通讯软件上，与这些平台/软件上的用户互动。
Coze 具有以下功能及优势：
Coze 提供了丰富的插件集合，可以扩展你的 Bot 的能力。用户也可进行插件的自定义，将现有的 API 能力通过配置的方式让 Bot 进行调用。 提供了知识库功能来管理和存储数据，可以让 Bot 使用知识库的内容进行回答。 长期记忆能力，Coze 提供了用于长期记忆的数据库功能，Bot 可以持久化的记住用户输入的参数和内容。 定时任务支持，Coze 支持为 Bot 创建定时任务，无需编写任何代码，只需输入任务描述，Bot 会暗示执行任务。 工作流，Coze 支持通过可视化的方式来创建工作流。 多 Agent 支持 Coze 有国内版 (www.coze.cn) 和国际版\[www.coze.com\]，本篇文章使用国际版进行介绍如何创建一个 Bot。
创建 Bot 注册完 Coze 账号，先创建 Bot，点击 Create Bot
输入 Bot 名称，这里由于想搭建一个 blog 助手，于是输入 Blog Assistant，然后上次 Bot 图像，如果没有合适的图像，也可以使用 DALL·E-3 生成头像。
设置 创建完 Bot 后，就进入 Bot 的设置页面。
...

 [post link to 使用 Coze 打造专属 AI Bot](https://jasminides.com/posts/cozebot/) [Go to Top (Alt + G)](https://jasminides.com/tags/bot/#top "Go to Top (Alt + G)")

## AI Bot Development
前言 Coze 是新一代一站式 AI Bot 开发平台。无论你是否有编程基础，都可以在 Coze 平台上快速搭建基于 AI 模型的各类问答 Bot，从解决简单的问答到处理复杂逻辑的对话。并且，你可以将搭建的 Bot 发布到各类社交平台和通讯软件上，与这些平台/软件上的用户互动。
Coze 具有以下功能及优势：
Coze 提供了丰富的插件集合，可以扩展你的 Bot 的能力。用户也可进行插件的自定义，将现有的 API 能力通过配置的方式让 Bot 进行调用。 提供了知识库功能来管理和存储数据，可以让 Bot 使用知识库的内容进行回答。 长期记忆能力，Coze 提供了用于长期记忆的数据库功能，Bot 可以持久化的记住用户输入的参数和内容。 定时任务支持，Coze 支持为 Bot 创建定时任务，无需编写任何代码，只需输入任务描述，Bot 会暗示执行任务。 工作流，Coze 支持通过可视化的方式来创建工作流。 多 Agent 支持 Coze 有国内版 (www.coze.cn) 和国际版\[www.coze.com\]，本篇文章使用国际版进行介绍如何创建一个 Bot。
创建 Bot 注册完 Coze 账号，先创建 Bot，点击 Create Bot
输入 Bot 名称，这里由于想搭建一个 blog 助手，于是输入 Blog Assistant，然后上次 Bot 图像，如果没有合适的图像，也可以使用 DALL·E-3 生成头像。
设置 创建完 Bot 后，就进入 Bot 的设置页面。
...

 [post link to 使用 Coze 打造专属 AI Bot](https://jasminides.com/posts/cozebot/) [Go to Top (Alt + G)](https://jasminides.com/tags/coze/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fcoze%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801915532&bpp=3&bdt=168&idt=127&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=4353464102998&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C42531706%2C95344787&oid=2&pvsid=323691172880460&tmod=9779448&uas=0&nvt=1&fsapi=1&fc=1920&brdim=70%2C70%2C70%2C70%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=178)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## AI Bot Creation Guide
目录

- [前言](https://jasminides.com/posts/cozebot/#%e5%89%8d%e8%a8%80)
- [创建 Bot](https://jasminides.com/posts/cozebot/#%e5%88%9b%e5%bb%ba-bot)
- [设置](https://jasminides.com/posts/cozebot/#%e8%ae%be%e7%bd%ae)
  - [设置大语言模型](https://jasminides.com/posts/cozebot/#%e8%ae%be%e7%bd%ae%e5%a4%a7%e8%af%ad%e8%a8%80%e6%a8%a1%e5%9e%8b)
  - [设置 Bot 的提示词](https://jasminides.com/posts/cozebot/#%e8%ae%be%e7%bd%ae-bot-%e7%9a%84%e6%8f%90%e7%a4%ba%e8%af%8d)
  - [skills](https://jasminides.com/posts/cozebot/#skills)
  - [Knowledge](https://jasminides.com/posts/cozebot/#knowledge)
  - [Memory](https://jasminides.com/posts/cozebot/#memory)
    - [Variable](https://jasminides.com/posts/cozebot/#variable)
  - [Database](https://jasminides.com/posts/cozebot/#database)
  - [Dialog](https://jasminides.com/posts/cozebot/#dialog)
  - [Preview](https://jasminides.com/posts/cozebot/#preview)
  - [Publish](https://jasminides.com/posts/cozebot/#publish)
- [小结](https://jasminides.com/posts/cozebot/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/cozebot/#%e5%8f%82%e8%80%83)

## 前言

Coze 是新一代一站式 AI Bot 开发平台。无论你是否有编程基础，都可以在 Coze 平台上快速搭建基于 AI 模型的各类问答 Bot，从解决简单的问答到处理复杂逻辑的对话。并且，你可以将搭建的 Bot 发布到各类社交平台和通讯软件上，与这些平台/软件上的用户互动。

Coze 具有以下功能及优势：

- Coze 提供了丰富的插件集合，可以扩展你的 Bot 的能力。用户也可进行插件的自定义，将现有的 API 能力通过配置的方式让 Bot 进行调用。
- 提供了知识库功能来管理和存储数据，可以让 Bot 使用知识库的内容进行回答。
- 长期记忆能力，Coze 提供了用于长期记忆的数据库功能，Bot 可以持久化的记住用户输入的参数和内容。
- 定时任务支持，Coze 支持为 Bot 创建定时任务，无需编写任何代码，只需输入任务描述，Bot 会暗示执行任务。
- 工作流，Coze 支持通过可视化的方式来创建工作流。
- 多 Agent 支持

Coze 有国内版 ( [www.coze.cn](https://www.coze.cn/)) 和国际版\[www.coze.com\]，本篇文章使用国际版进行介绍如何创建一个 Bot。

## 创建 Bot

注册完 Coze 账号，先创建 Bot，点击 Create Bot

![alt text](https://jasminides.com/img/coze-bot/image.png)

输入 Bot 名称，这里由于想搭建一个 blog 助手，于是输入 Blog Assistant，然后上次 Bot 图像，如果没有合适的图像，也可以使用 DALL·E-3 生成头像。

## 设置

创建完 Bot 后，就进入 Bot 的设置页面。

![alt text](https://jasminides.com/img/coze-bot/image-1.png)

接下来分别会介绍界面上的功能：

### 设置大语言模型

图中 1 处这里可以设置大语言模型，可以选择不同的模型，有刚发布的 GPT-4o 等，并可进行相应的参数设置，这里我们选择 GPT-4o ,不修改默认设置。

![alt text](https://jasminides.com/img/coze-bot/image-2.png)

### 设置 Bot 的提示词

图中 2 处是重要的一环，编写提示词 prompt，好的提示词可以让大语言模型更好理解用户的输入。

我们先简单输入一段提示词：
`你是一名知识渊博的助理，专门负责 Overstarry 的博客。你的技能是回答有关博客内容的询问，并引导用户全面了解博客内容。`

然后使用 Optimize 可以让大语言模型进行优化提示词。根据优化后的提示词进行修改，最后的提示词如下：

```text
# 角色
你是一个对 Overstarry 博客有深入了解的知识渊博的助理。你对博客的所有内容和信息都拥有绝对的熟悉度。

## 技能
### 技能 1：回答关于博客内容的询问
- 当用户关于博客内容提出疑问时，提供详尽准确的答复。你的回答应该围绕博客主题，鼓励和指引用户深入了解更多的博客内容。

### 技能 2：详细介绍博客内容
- 根据用户需求，深入介绍博客的各个方面，无论是主题、风格、写作技巧，还是特别的内容。

### 技能 3：引导用户全面了解博客
- 通过提供概要、提示或者直接回答用户问题，引导用户全面、深入地阅读和理解博客。

## 约束：
- 只讨论与博客内容相关的话题。
- 坚持提供精确、清晰、轻松理解的答案。
- 根据用户希望了解的信息做出有针对性的回应。
- 不要涉及任何与博客无关的信息。

```

复制

![alt text](https://jasminides.com/img/coze-bot/image-3.png)

### skills

设定完 Bot 的角色及技能后，我们可以通过 skills 功能加强 Bot 的能力。

![alt text](https://jasminides.com/img/coze-bot/image-4.png)

![alt text](https://jasminides.com/img/coze-bot/image-5.png)

本文只使用了 Coze 的插件功能，我们添加 `Google Web Search` 和 `Browser`,添加完插件后我们还得修改提示词，不然 Bot 不会使用 插件进行搜索。

```#
你是一个对Overstarry博客有深度了解的资深助理。你精通博客的所有内容和数据。

## 技能
### 技能 1：回答博客内容的问题
- 通过browse(url: "overstarry.vip")全面理解用户查询并生成正确的答案。
- 如果不熟悉某一博客条目，转用googleWebSearch("overstarry.vip + inquiry")来寻找合适的答案。

### 技能 2：全方位介绍博客内容
- 根据用户需求，深入浅出地介绍博客的各个方面——主题、风格、写作技巧或特色内容。

### 技能 3：引导用户全方位理解博客
- 通过提供大纲、点醒或直接回答用户问题，引导用户深入、全面地浏览和理解博客。

## 约束：
- 只讨论与博客内容相关的话题。
- 始终提供精确、易懂、清晰的答案。
- 针对性地回应用户需求的信息。
- 避免涉及任何与博客无关的信息。
复制
```

### Knowledge

Knowledge 可以设置 Bot 的知识库，可以通过接口和上传文件的方式，让 Bot 通过知识库的内容更好更精确的回答用户的问题

### Memory

#### Variable

可以通过使用变量功能记录用户偏好或行为，例如记录用户的语言偏好

![alt text](https://jasminides.com/img/coze-bot/image-6.png)

### Database

Database 可以通过创建数据表的方式，将用户询问中的一些数据记录下来，这里我们创建一个记录 tag 和文章列表的数据表

![alt text](https://jasminides.com/img/coze-bot/image-7.png)

### Dialog

Dialog 是设定一些 Bot 的常规参数，如 Bot 的开场白，以及是否根据上下文提供 3 个选项等功能。

### Preview

Preview 面板是用来进行测试用的，配置好 Bot 后，可以在此处进行测试 Bot 是否符合预期。

![alt text](https://jasminides.com/img/coze-bot/image-8.png)

### Publish

Publish 可以将你调试好的 bot 发布到商店和其它 IM 平台。

![alt text](https://jasminides.com/img/coze-bot/image-9.png)

## 小结

本文介绍了如何使用 coze 平台搭建专属的 AI bot。本文创建的 bot 已发布到 store 中，感兴趣的小伙伴可以通过 [https://www.coze.com/store/bot/7375447781130960903?panel=1](https://www.coze.com/store/bot/7375447781130960903?panel=1) 访问。

## 参考

- [https://www.coze.com/docs/guides/welcome?\_lang=zh](https://www.coze.com/docs/guides/welcome?_lang=zh)
- [https://overstarry.vip/](https://overstarry.vip/)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fcozebot%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/cozebot/#top "Go to Top (Alt + G)")

## Golang Slug Generation
目录

- [slug 介绍](https://jasminides.com/posts/go_generate_slug/#slug-%e4%bb%8b%e7%bb%8d)
- [安装](https://jasminides.com/posts/go_generate_slug/#%e5%ae%89%e8%a3%85)
- [使用](https://jasminides.com/posts/go_generate_slug/#%e4%bd%bf%e7%94%a8)
- [参考](https://jasminides.com/posts/go_generate_slug/#%e5%8f%82%e8%80%83)

## slug 介绍

slug 在不同的场景有不同的意义，在 URL 中表示一种用于描述资源的短简洁易于理解的资源描述符，在数据库系统中还可以用于描述资源的唯一标识符，总的来说 slug 可以用来标识和描述资源的文本标识符，有很好的可读性和唯一性。

本文将介绍 golang 中如何根据字符串生成相应的 slug 文本。

## 安装

执行 `go get -u github.com/gosimple/slug` 来安装 slug

## 使用

先介绍 slug 库的基础使用方法：

```go
package main

import (
	"fmt"
	"github.com/gosimple/slug"
)

func main() {
	text := slug.Make("overstarry home")
	fmt.Println(text)
	text = slug.Make("text generate")
	fmt.Println(text)
}

```

复制

运行后：

```console
overstarry-home
text-generate

```

复制

除了基础的转换功能，slug 还支持将不同的语言进行转换，查看下面的例子：

```go
func main() {
	text := slug.Make("overstarry home")
	fmt.Println(text)
	text = slug.Make("text generate")
	fmt.Println(text)
	text = slug.Make("Hellö Wörld хелло ворлд")
	fmt.Println(text)

	someText := slug.Make("影師")
	fmt.Println(someText)
    enText := slug.MakeLang("This & that", "en")
	fmt.Println(enText)
}

```

复制

```console
overstarry-home
text-generate
hello-world-khello-vorld
ping-guo
this-and-that

```

复制

如果想要保留大写字母，可以设置 slug.Lowercase 参数来实现。如果想实现自定义的替换可以使用 slug.CustomSub 来实现。

## 参考

- [https://pkg.go.dev/github.com/gosimple/slug](https://pkg.go.dev/github.com/gosimple/slug)
- [https://www.practical-go-lessons.com/post/how-to-create-a-slug-with-go-c9msh2glarts70kje1ag](https://www.practical-go-lessons.com/post/how-to-create-a-slug-with-go-c9msh2glarts70kje1ag)
- [https://github.com/gosimple/slug](https://github.com/gosimple/slug)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fgo_generate_slug%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/go_generate_slug/#top "Go to Top (Alt + G)")

## Golang Slug Generation
slug 介绍 slug 在不同的场景有不同的意义，在 URL 中表示一种用于描述资源的短简洁易于理解的资源描述符，在数据库系统中还可以用于描述资源的唯一标识符，总的来说 slug 可以用来标识和描述资源的文本标识符，有很好的可读性和唯一性。
本文将介绍 golang 中如何根据字符串生成相应的 slug 文本。
安装 执行 go get -u github.com/gosimple/slug 来安装 slug
使用 先介绍 slug 库的基础使用方法：
package main import ( "fmt" "github.com/gosimple/slug" ) func main() { text := slug.Make("overstarry home") fmt.Println(text) text = slug.Make("text generate") fmt.Println(text) } 运行后：
overstarry-home text-generate 除了基础的转换功能，slug 还支持将不同的语言进行转换，查看下面的例子：
func main() { text := slug.Make("overstarry home") fmt.Println(text) text = slug.Make("text generate") fmt.Println(text) text = slug.Make("Hellö Wörld хелло ворлд") fmt.Println(text) someText := slug.Make("影師") fmt.Println(someText) enText := slug.MakeLang("This & that", "en") fmt.Println(enText) } overstarry-home text-generate hello-world-khello-vorld ping-guo this-and-that 如果想要保留大写字母，可以设置 slug.Lowercase 参数来实现。如果想实现自定义的替换可以使用 slug.CustomSub 来实现。
...

 [post link to golang 生成 slug 字符串](https://jasminides.com/posts/go_generate_slug/) [Go to Top (Alt + G)](https://jasminides.com/tags/slug/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fslug%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801915554&bpp=15&bdt=175&idt=179&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=1606185737418&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340&oid=2&pvsid=2184076593632518&tmod=238615074&uas=0&nvt=1&fsapi=1&fc=1920&brdim=100%2C100%2C100%2C100%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=197)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Metabase Data Visualization
前言 前面的文章介绍过一个开源的大数据可视化工具 \- Apache Superset，本文将介绍作者最近了解到的另一个可视化工具 Metabase。
Metabase 介绍 Metabase 是一个简单易用的开源项目，旨在为公司中的每个人提供商业智能和分析的最简单、最快捷的方法。Metabase 具有以下核心优势和主要功能：
短时间内完成设置。 团队成员不需要 SQL 知识基础。 提供 SQL 编辑器来进行更复杂的查询。 构建漂亮、交互式的仪表盘，包括过滤器、自动刷新、全屏显示和自定义点击行为等功能。 定义规范的细分和指标供团队使用 使用仪表板订阅按计划将数据发送到 Slack 或发送电子邮件。 设置警报，让数据更改时通知您。 在应用程序中嵌入图表及仪表盘。 配置了细粒度的数据权限功能，方便进行数据安全控制。 安装 接下来介绍如何安装 Metabase，我们将使用 docker 部署的方式进行安装。
docker-compose.yaml 内容如下：
version: '3.9' services: metabase: image: metabase/metabase:latest container\_name: metabase hostname: metabase volumes: - /dev/urandom:/dev/random:ro ports: - 3000:3000 environment: MB\_DB\_TYPE: postgres MB\_DB\_DBNAME: metabaseappdb MB\_DB\_PORT: 5432 MB\_DB\_USER: metabase MB\_DB\_PASS: mysecretpassword MB\_DB\_HOST: postgres networks: - metanet1 healthcheck: test: curl --fail -I http://localhost:3000/api/health \|\| exit 1 interval: 15s timeout: 5s retries: 5 postgres: image: postgres:latest container\_name: postgres hostname: postgres environment: POSTGRES\_USER: metabase POSTGRES\_DB: metabaseappdb POSTGRES\_PASSWORD: mysecretpassword networks: - metanet1 networks: metanet1: driver: bridge 执行 docker compose up -d 即可启动服务。接下来访问 http://127.0.0.1:3000/ 进行安装，设置完语言密码默认数据库，安装即算完成。
...

 [post link to metabase 介绍及简单使用](https://jasminides.com/posts/metabase/) [Go to Top (Alt + G)](https://jasminides.com/tags/data-visualization/#top "Go to Top (Alt + G)")

## Metabase Overview
前言 前面的文章介绍过一个开源的大数据可视化工具 \- Apache Superset，本文将介绍作者最近了解到的另一个可视化工具 Metabase。
Metabase 介绍 Metabase 是一个简单易用的开源项目，旨在为公司中的每个人提供商业智能和分析的最简单、最快捷的方法。Metabase 具有以下核心优势和主要功能：
短时间内完成设置。 团队成员不需要 SQL 知识基础。 提供 SQL 编辑器来进行更复杂的查询。 构建漂亮、交互式的仪表盘，包括过滤器、自动刷新、全屏显示和自定义点击行为等功能。 定义规范的细分和指标供团队使用 使用仪表板订阅按计划将数据发送到 Slack 或发送电子邮件。 设置警报，让数据更改时通知您。 在应用程序中嵌入图表及仪表盘。 配置了细粒度的数据权限功能，方便进行数据安全控制。 安装 接下来介绍如何安装 Metabase，我们将使用 docker 部署的方式进行安装。
docker-compose.yaml 内容如下：
version: '3.9' services: metabase: image: metabase/metabase:latest container\_name: metabase hostname: metabase volumes: - /dev/urandom:/dev/random:ro ports: - 3000:3000 environment: MB\_DB\_TYPE: postgres MB\_DB\_DBNAME: metabaseappdb MB\_DB\_PORT: 5432 MB\_DB\_USER: metabase MB\_DB\_PASS: mysecretpassword MB\_DB\_HOST: postgres networks: - metanet1 healthcheck: test: curl --fail -I http://localhost:3000/api/health \|\| exit 1 interval: 15s timeout: 5s retries: 5 postgres: image: postgres:latest container\_name: postgres hostname: postgres environment: POSTGRES\_USER: metabase POSTGRES\_DB: metabaseappdb POSTGRES\_PASSWORD: mysecretpassword networks: - metanet1 networks: metanet1: driver: bridge 执行 docker compose up -d 即可启动服务。接下来访问 http://127.0.0.1:3000/ 进行安装，设置完语言密码默认数据库，安装即算完成。
...

 [post link to metabase 介绍及简单使用](https://jasminides.com/posts/metabase/) [Go to Top (Alt + G)](https://jasminides.com/tags/metabase/#top "Go to Top (Alt + G)")

## Metabase Data Visualization
目录

- [前言](https://jasminides.com/posts/metabase/#%e5%89%8d%e8%a8%80)
- [Metabase 介绍](https://jasminides.com/posts/metabase/#metabase-%e4%bb%8b%e7%bb%8d)
- [安装](https://jasminides.com/posts/metabase/#%e5%ae%89%e8%a3%85)
- [添加数据库](https://jasminides.com/posts/metabase/#%e6%b7%bb%e5%8a%a0%e6%95%b0%e6%8d%ae%e5%ba%93)
- [浏览数据表](https://jasminides.com/posts/metabase/#%e6%b5%8f%e8%a7%88%e6%95%b0%e6%8d%ae%e8%a1%a8)
- [可视化](https://jasminides.com/posts/metabase/#%e5%8f%af%e8%a7%86%e5%8c%96)
  - [可视化查询](https://jasminides.com/posts/metabase/#%e5%8f%af%e8%a7%86%e5%8c%96%e6%9f%a5%e8%af%a2)
  - [SQL 编辑器](https://jasminides.com/posts/metabase/#sql--%e7%bc%96%e8%be%91%e5%99%a8)
- [仪表盘](https://jasminides.com/posts/metabase/#%e4%bb%aa%e8%a1%a8%e7%9b%98)
- [小结](https://jasminides.com/posts/metabase/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/metabase/#%e5%8f%82%e8%80%83)

## 前言

前面的文章介绍过一个开源的大数据可视化工具 \- Apache Superset，本文将介绍作者最近了解到的另一个可视化工具 Metabase。

## Metabase 介绍

Metabase 是一个简单易用的开源项目，旨在为公司中的每个人提供商业智能和分析的最简单、最快捷的方法。Metabase 具有以下核心优势和主要功能：

- 短时间内完成设置。
- 团队成员不需要 SQL 知识基础。
- 提供 SQL 编辑器来进行更复杂的查询。
- 构建漂亮、交互式的仪表盘，包括过滤器、自动刷新、全屏显示和自定义点击行为等功能。
- 定义规范的细分和指标供团队使用
- 使用仪表板订阅按计划将数据发送到 Slack 或发送电子邮件。
- 设置警报，让数据更改时通知您。
- 在应用程序中嵌入图表及仪表盘。
- 配置了细粒度的数据权限功能，方便进行数据安全控制。

## 安装

接下来介绍如何安装 Metabase，我们将使用 docker 部署的方式进行安装。

docker-compose.yaml 内容如下：

```yaml
version: '3.9'
services:
  metabase:
    image: metabase/metabase:latest
    container_name: metabase
    hostname: metabase
    volumes:
    - /dev/urandom:/dev/random:ro
    ports:
      - 3000:3000
    environment:
      MB_DB_TYPE: postgres
      MB_DB_DBNAME: metabaseappdb
      MB_DB_PORT: 5432
      MB_DB_USER: metabase
      MB_DB_PASS: mysecretpassword
      MB_DB_HOST: postgres
    networks:
      - metanet1
    healthcheck:
      test: curl --fail -I http://localhost:3000/api/health || exit 1
      interval: 15s
      timeout: 5s
      retries: 5
  postgres:
    image: postgres:latest
    container_name: postgres
    hostname: postgres
    environment:
      POSTGRES_USER: metabase
      POSTGRES_DB: metabaseappdb
      POSTGRES_PASSWORD: mysecretpassword
    networks:
      - metanet1
networks:
  metanet1:
    driver: bridge

```

复制

执行 docker compose up -d 即可启动服务。接下来访问 `http://127.0.0.1:3000/` 进行安装，设置完语言密码默认数据库，安装即算完成。

![alt text](https://jasminides.com/img/metabase/image.png)

## 添加数据库

在 Metabase 的管理后台我们可以进行数据库的添加，可以看到相较于 Superset Metabase 支持的数据源不够多。填写完相关信息，点击保存会进行连接的测试，连接成功就可以在数据源列表中看到。

![alt text](https://jasminides.com/img/metabase/image-1.png)

## 浏览数据表

添加完数据库，我们可以查看添加的数据库中的数据表。

![alt text](https://jasminides.com/img/metabase/image-2.png)

## 可视化

添加完数据源，查看了数据表，接下来进行可视化的介绍，Metabase 提供了两种可视化的方式:1) 可视化查询 2) SQL 语句查询。

### 可视化查询

在浏览数据表时，点击右上角的 创建 按钮，然后选择 问题，即可进入查询构建页面。简单来说就是将 SQL 的语句转换为表单的填写控制。右上角可以查看相应的 SQL 语句。点击可视化就会生成相应的图表。

![alt text](https://jasminides.com/img/metabase/image-3.png)![alt text](https://jasminides.com/img/metabase/image-4.png)![alt text](https://jasminides.com/img/metabase/image-5.png)

### SQL 编辑器

熟悉 SQL 的可使用 SQL 编辑器功能，同样点击右上角的 创建 按钮，然后选择 SQL 查询，选择相应的数据源，输入语句并运行，同样会生成相应的图表。

![alt text](https://jasminides.com/img/metabase/image-6.png)

## 仪表盘

在分析中心可以创建仪表盘，并将前面创建的可视化图表添加进仪表盘中，并可对仪表盘进行排列调整，方便打造美观的布局效果。

![alt text](https://jasminides.com/img/metabase/image-6.png)

## 小结

本文简单的介绍了 Metabase 开源可视化平台的安装及使用，Metabase 的一些复杂的功能，感兴趣的读者可自行学习研究。

## 参考

- [https://www.metabase.com/docs/latest/](https://www.metabase.com/docs/latest/)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fmetabase%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/metabase/#top "Go to Top (Alt + G)")

## Metabase Visualization Tool
前言 前面的文章介绍过一个开源的大数据可视化工具 \- Apache Superset，本文将介绍作者最近了解到的另一个可视化工具 Metabase。
Metabase 介绍 Metabase 是一个简单易用的开源项目，旨在为公司中的每个人提供商业智能和分析的最简单、最快捷的方法。Metabase 具有以下核心优势和主要功能：
短时间内完成设置。 团队成员不需要 SQL 知识基础。 提供 SQL 编辑器来进行更复杂的查询。 构建漂亮、交互式的仪表盘，包括过滤器、自动刷新、全屏显示和自定义点击行为等功能。 定义规范的细分和指标供团队使用 使用仪表板订阅按计划将数据发送到 Slack 或发送电子邮件。 设置警报，让数据更改时通知您。 在应用程序中嵌入图表及仪表盘。 配置了细粒度的数据权限功能，方便进行数据安全控制。 安装 接下来介绍如何安装 Metabase，我们将使用 docker 部署的方式进行安装。
docker-compose.yaml 内容如下：
version: '3.9' services: metabase: image: metabase/metabase:latest container\_name: metabase hostname: metabase volumes: - /dev/urandom:/dev/random:ro ports: - 3000:3000 environment: MB\_DB\_TYPE: postgres MB\_DB\_DBNAME: metabaseappdb MB\_DB\_PORT: 5432 MB\_DB\_USER: metabase MB\_DB\_PASS: mysecretpassword MB\_DB\_HOST: postgres networks: - metanet1 healthcheck: test: curl --fail -I http://localhost:3000/api/health \|\| exit 1 interval: 15s timeout: 5s retries: 5 postgres: image: postgres:latest container\_name: postgres hostname: postgres environment: POSTGRES\_USER: metabase POSTGRES\_DB: metabaseappdb POSTGRES\_PASSWORD: mysecretpassword networks: - metanet1 networks: metanet1: driver: bridge 执行 docker compose up -d 即可启动服务。接下来访问 http://127.0.0.1:3000/ 进行安装，设置完语言密码默认数据库，安装即算完成。
...

 [post link to metabase 介绍及简单使用](https://jasminides.com/posts/metabase/) [Go to Top (Alt + G)](https://jasminides.com/tags/visualization/#top "Go to Top (Alt + G)")

## Generate Analytics ID
目录

- [Google Analytics 介绍](https://jasminides.com/posts/gogenerategaid/#google-analytics-%e4%bb%8b%e7%bb%8d)
- [配置](https://jasminides.com/posts/gogenerategaid/#%e9%85%8d%e7%bd%ae)
  - [启用 API](https://jasminides.com/posts/gogenerategaid/#%e5%90%af%e7%94%a8-api)
  - [配置服务账号](https://jasminides.com/posts/gogenerategaid/#%e9%85%8d%e7%bd%ae%e6%9c%8d%e5%8a%a1%e8%b4%a6%e5%8f%b7)
  - [安装 go 客户端](https://jasminides.com/posts/gogenerategaid/#%e5%ae%89%e8%a3%85-go-%e5%ae%a2%e6%88%b7%e7%ab%af)
  - [生成流程](https://jasminides.com/posts/gogenerategaid/#%e7%94%9f%e6%88%90%e6%b5%81%e7%a8%8b)
  - [代码](https://jasminides.com/posts/gogenerategaid/#%e4%bb%a3%e7%a0%81)
- [小结](https://jasminides.com/posts/gogenerategaid/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/gogenerategaid/#%e5%8f%82%e8%80%83)

## Google Analytics 介绍

Google Analytics（分析）4 是一项分析服务，用于衡量您的网站和应用中的流量和互动情况。本文将介绍如何通过调用 Google Analytics admin API 来生成 Google Analytics 衡量 ID.

## 配置

### 启用 API

在 Google Cloud console 后台 API 和服务 启用 Google Analytics Admin API。

### 配置服务账号

为了调用 API，我们需要创建一个服务账号，然后为创建的服务账号添加密钥。

![alt text](https://jasminides.com/img/googleanalyticsid/image.png)

![alt text](https://jasminides.com/img/googleanalyticsid/image-1.png)

需要注意的是还需要在 Google Analytics 为服务账号添加权限，不然请求接口会没数据。

### 安装 go 客户端

接下来安装 go 客户端：

```shell
go get google.golang.org/api/analyticsadmin/v1alpha

```

复制

### 生成流程

接下来我们会按照常规的 id 生成流程编写相应的代码，流程:
1 获取账号信息

通过 List 接口获取当前服务账号所拥有的所有 Google Analytics 账户信息。

```go
    accountsService := analyticsadmin.NewAccountsService(service)
	accountsReply, err := accountsService.List().Do();
	if err != nil {
		log.Fatal("list account err",err)
		return
	}
	for _,acc := range accountsReply.Accounts {
		fmt.Println(acc.Name)
	}

```

复制

2 创建媒体资源

通过 List 接口获得第一个账号的所有媒体资源信息，并通过 Create 接口创建一个新的媒体资源。

```go
    propertiesService := analyticsadmin.NewPropertiesService(service)
	propertiesReply,err := propertiesService.List().Filter(fmt.Sprintf("parent:%s",accountsReply.Accounts[0].Name)).Do()
	if err != nil {
		log.Fatal("list properties err",err)
		return
	}
	for _,pro := range propertiesReply.Properties {
		fmt.Println(pro)
	}
	propertie,err := propertiesService.Create(&analyticsadmin.GoogleAnalyticsAdminV1betaProperty{
		Account:         accountsReply.Accounts[0].Name,
		CurrencyCode:     "CNY",
		DisplayName:      "overstarrytest",
		// 行业类型
		IndustryCategory: "ONLINE_COMMUNITIES",
		Parent:           accountsReply.Accounts[0].Name,
		PropertyType:     "PROPERTY_TYPE_ORDINARY",
		TimeZone:         "Asia/Shanghai",
	}).Do()
	if err != nil {
		log.Fatal("create  propertie err",err)
		return

	}

```

复制

3 设置数据流

接下来通过上面创建的媒体渠道创建新的数据流。

```go
    propertiesDataStreamsService  := analyticsadmin.NewPropertiesDataStreamsService(service)
	res,err := propertiesDataStreamsService.Create(propertie.Name,&analyticsadmin.GoogleAnalyticsAdminV1betaDataStream{
		DisplayName:          "测试链接",
		Type:                 "WEB_DATA_STREAM",
		WebStreamData:        &analyticsadmin.GoogleAnalyticsAdminV1betaDataStreamWebStreamData{
			DefaultUri:      "https://www.overstarry.vip",
			MeasurementId:   "",
		},
	}).Do()
	fmt.Printf("%v",res.WebStreamData.MeasurementId)

```

复制

### 代码

完整代码如下：
![alt text](https://jasminides.com/img/googleanalyticsid/carbon.png)

运行代码：
![alt text](https://jasminides.com/img/googleanalyticsid/image-2.png)

可以看到衡量 id 顺利产生。

## 小结

本文简单介绍了如何通过代码调用 analyticsadmin api 接口快速简单的生成衡量 id，相关的代码可以在 [https://github.com/overstarry/google-analytics-id-generate](https://github.com/overstarry/google-analytics-id-generate) 找到。

## 参考

- [https://developers.google.com/analytics/devguides/config/admin/v1?hl=zh-cn](https://developers.google.com/analytics/devguides/config/admin/v1?hl=zh-cn)
- [https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties?hl=zh-cn#IndustryCategory](https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties?hl=zh-cn#IndustryCategory)
- [https://github.com/overstarry/google-analytics-id-generate](https://github.com/overstarry/google-analytics-id-generate)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fgogenerategaid%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/gogenerategaid/#top "Go to Top (Alt + G)")

## Google Analytics Measurement ID Guide
Google Analytics 介绍 Google Analytics（分析）4 是一项分析服务，用于衡量您的网站和应用中的流量和互动情况。本文将介绍如何通过调用 Google Analytics admin API 来生成 Google Analytics 衡量 ID.
配置 启用 API 在 Google Cloud console 后台 API 和服务 启用 Google Analytics Admin API。
配置服务账号 为了调用 API，我们需要创建一个服务账号，然后为创建的服务账号添加密钥。
需要注意的是还需要在 Google Analytics 为服务账号添加权限，不然请求接口会没数据。
安装 go 客户端 接下来安装 go 客户端：
go get google.golang.org/api/analyticsadmin/v1alpha 生成流程 接下来我们会按照常规的 id 生成流程编写相应的代码，流程: 1 获取账号信息
通过 List 接口获取当前服务账号所拥有的所有 Google Analytics 账户信息。
accountsService := analyticsadmin.NewAccountsService(service) accountsReply, err := accountsService.List().Do(); if err != nil { log.Fatal("list account err",err) return } for \_,acc := range accountsReply.Accounts { fmt.Println(acc.Name) } 2 创建媒体资源
...

 [post link to Go 生成 Google analytics 衡量 ID](https://jasminides.com/posts/gogenerategaid/) [Go to Top (Alt + G)](https://jasminides.com/tags/google-analytics/#top "Go to Top (Alt + G)")

## Docker Init Command
目录

- [前言](https://jasminides.com/posts/docker_init_command/#%e5%89%8d%e8%a8%80)
- [docker init 简介](https://jasminides.com/posts/docker_init_command/#docker-init-%e7%ae%80%e4%bb%8b)
- [使用](https://jasminides.com/posts/docker_init_command/#%e4%bd%bf%e7%94%a8)
- [小结](https://jasminides.com/posts/docker_init_command/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/docker_init_command/#%e5%8f%82%e8%80%83)

## 前言

Docker 是一个广受欢迎的开发平台，它允许用户通过容器化技术来构建、打包和部署应用程序。尽管 Docker 提供了强大的功能和灵活性，但对于初学者而言，在项目中配置 Docker 可能会遇到一些挑战。

不过，Docker 官方为了降低使用门槛，推出了一个便捷的命令 `docker init`。这个命令旨在快速初始化 Docker 配置，从而简化将 Docker 集成到项目中的流程。通过使用这个命令，用户可以轻松地为项目设置必要的 Docker 支持，进而享受到 Docker 带来的便利和效率提升。

## docker init 简介

docker init 命令会根据用户指定的选项生成运行容器的一些文件，极大的加快了项目的容器化：

- .dockerignore : docker 构建时忽略的文件列表
- Dockerfile: 镜像的核心文件
- Compose.yaml: docker compose 的配置文件
- README.Docker.md

如果你的项目中已有以上文件，会让你选择是否覆盖旧文件避免文件冲突问题。

docker init 提供了一组项目的模板文件，包括了 Go、Python、ASP.NET Core 等常见的服务器应用程序及一个其它类型应用程序模板。开发者使用 init 命令时，可以根据选择的模板生成相应的文件，使开发者可以快速的构建并启动容器。

## 使用

接下来介绍如何使用 docker init 进行项目容器的初始化，这里以前文的 go 项目为例子进行介绍。

进入项目根目录执行 init 命令，选择 go 模板，会让你选择使用的 go 版本，主程序的位置及应用所使用的端口：
![alt text](https://jasminides.com/img/docker-init/image.png)![alt text](https://jasminides.com/img/docker-init/image-1.png)

执行完可以看到会生成相应的文件及如何构建并运行的命令。

查看生成的 Dockerfile 和 Compose.yaml 文件：

```Dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

################################################################################
# Create a stage for building the application.
ARG GO_VERSION=1.21.0
FROM --platform=$BUILDPLATFORM golang:${GO_VERSION} AS build
WORKDIR /src

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /go/pkg/mod/ to speed up subsequent builds.
# Leverage bind mounts to go.sum and go.mod to avoid having to copy them into
# the container.
RUN --mount=type=cache,target=/go/pkg/mod/ \
    --mount=type=bind,source=go.sum,target=go.sum \
    --mount=type=bind,source=go.mod,target=go.mod \
    go mod download -x

# This is the architecture you’re building for, which is passed in by the builder.
# Placing it here allows the previous steps to be cached across architectures.
ARG TARGETARCH

# Build the application.
# Leverage a cache mount to /go/pkg/mod/ to speed up subsequent builds.
# Leverage a bind mount to the current directory to avoid having to copy the
# source code into the container.
RUN --mount=type=cache,target=/go/pkg/mod/ \
    --mount=type=bind,target=. \
    CGO_ENABLED=0 GOARCH=$TARGETARCH go build -o /bin/server ./retry/server

################################################################################
# Create a new stage for running the application that contains the minimal
# runtime dependencies for the application. This often uses a different base
# image from the build stage where the necessary files are copied from the build
# stage.
#
# The example below uses the alpine image as the foundation for running the app.
# By specifying the "latest" tag, it will also use whatever happens to be the
# most recent version of that image when you build your Dockerfile. If
# reproducability is important, consider using a versioned tag
# (e.g., alpine:3.17.2) or SHA (e.g., alpine@sha256:c41ab5c992deb4fe7e5da09f67a8804a46bd0592bfdf0b1847dde0e0889d2bff).
FROM alpine:latest AS final

# Install any runtime dependencies that are needed to run your application.
# Leverage a cache mount to /var/cache/apk/ to speed up subsequent builds.
RUN --mount=type=cache,target=/var/cache/apk \
    apk --update add \
        ca-certificates \
        tzdata \
        && \
        update-ca-certificates

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser

# Copy the executable from the "build" stage.
COPY --from=build /bin/server /bin/

# Expose the port that the application listens on.
EXPOSE 9000

# What the container should run when it is started.
ENTRYPOINT [ "/bin/server" ]

```

复制

可以看到 Dockerfile 是一个常见的多阶段构建镜像流程。

```yaml
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 9000:9000

# The commented out section below is an example of how to define a PostgreSQL
# database that your application can use. `depends_on` tells Docker Compose to
# start the database before your application. The `db-data` volume persists the
# database data between container restarts. The `db-password` secret is used
# to set the database password. You must create `db/password.txt` and add
# a password of your choosing to it before running `docker compose up`.
#     depends_on:
#       db:
#         condition: service_healthy
#   db:
#     image: postgres
#     restart: always
#     user: postgres
#     secrets:
#       - db-password
#     volumes:
#       - db-data:/var/lib/postgresql/data
#     environment:
#       - POSTGRES_DB=example
#       - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
#     expose:
#       - 5432
#     healthcheck:
#       test: [ "CMD", "pg_isready" ]
#       interval: 10s
#       timeout: 5s
#       retries: 5
# volumes:
#   db-data:
# secrets:
#   db-password:
#     file: db/password.txt

```

复制

docker-compose 文件也是常规的内容，可以看到文件中还提供了默认的数据库服务配置，使开发者可以快速的启动一个数据库服务。

## 小结

本文讲述了 docker 提供的一种快速生成 docker 镜像构建文件的命令：init ,通过这个命令使开发者能够快速方便的为项目启用容器能力。

## 参考

- [https://docs.docker.com/reference/cli/docker/init/](https://docs.docker.com/reference/cli/docker/init/)
- [https://www.docker.com/blog/docker-init-initialize-dockerfiles-and-compose-files-with-a-single-cli-command/](https://www.docker.com/blog/docker-init-initialize-dockerfiles-and-compose-files-with-a-single-cli-command/)
- [https://www.docker.com/blog/streamline-dockerization-with-docker-init-ga/](https://www.docker.com/blog/streamline-dockerization-with-docker-init-ga/)
- [https://www.youtube.com/watch?v=f4cHtDRZv5U](https://www.youtube.com/watch?v=f4cHtDRZv5U)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fdocker_init_command%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/docker_init_command/#top "Go to Top (Alt + G)")

## Docker Init Command
前言 Docker 是一个广受欢迎的开发平台，它允许用户通过容器化技术来构建、打包和部署应用程序。尽管 Docker 提供了强大的功能和灵活性，但对于初学者而言，在项目中配置 Docker 可能会遇到一些挑战。
不过，Docker 官方为了降低使用门槛，推出了一个便捷的命令docker init。这个命令旨在快速初始化 Docker 配置，从而简化将 Docker 集成到项目中的流程。通过使用这个命令，用户可以轻松地为项目设置必要的 Docker 支持，进而享受到 Docker 带来的便利和效率提升。
docker init 简介 docker init 命令会根据用户指定的选项生成运行容器的一些文件，极大的加快了项目的容器化：
.dockerignore : docker 构建时忽略的文件列表 Dockerfile: 镜像的核心文件 Compose.yaml: docker compose 的配置文件 README.Docker.md 如果你的项目中已有以上文件，会让你选择是否覆盖旧文件避免文件冲突问题。
docker init 提供了一组项目的模板文件，包括了 Go、Python、ASP.NET Core 等常见的服务器应用程序及一个其它类型应用程序模板。开发者使用 init 命令时，可以根据选择的模板生成相应的文件，使开发者可以快速的构建并启动容器。
使用 接下来介绍如何使用 docker init 进行项目容器的初始化，这里以前文的 go 项目为例子进行介绍。
进入项目根目录执行 init 命令，选择 go 模板，会让你选择使用的 go 版本，主程序的位置及应用所使用的端口： 执行完可以看到会生成相应的文件及如何构建并运行的命令。
查看生成的 Dockerfile 和 Compose.yaml 文件：
\# syntax=docker/dockerfile:1 # Comments are provided throughout this file to help you get started. # If you need more help, visit the Dockerfile reference guide at # https://docs.docker.com/go/dockerfile-reference/ # Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7 ################################################################################ # Create a stage for building the application. ARG GO\_VERSION=1.21.0 FROM --platform=$BUILDPLATFORM golang:${GO\_VERSION} AS build WORKDIR /src # Download dependencies as a separate step to take advantage of Docker's caching. # Leverage a cache mount to /go/pkg/mod/ to speed up subsequent builds. # Leverage bind mounts to go.sum and go.mod to avoid having to copy them into # the container. RUN --mount=type=cache,target=/go/pkg/mod/ \ --mount=type=bind,source=go.sum,target=go.sum \ --mount=type=bind,source=go.mod,target=go.mod \ go mod download -x # This is the architecture you’re building for, which is passed in by the builder. # Placing it here allows the previous steps to be cached across architectures. ARG TARGETARCH # Build the application. # Leverage a cache mount to /go/pkg/mod/ to speed up subsequent builds. # Leverage a bind mount to the current directory to avoid having to copy the # source code into the container. RUN --mount=type=cache,target=/go/pkg/mod/ \ --mount=type=bind,target=. \ CGO\_ENABLED=0 GOARCH=$TARGETARCH go build -o /bin/server ./retry/server ################################################################################ # Create a new stage for running the application that contains the minimal # runtime dependencies for the application. This often uses a different base # image from the build stage where the necessary files are copied from the build # stage. # # The example below uses the alpine image as the foundation for running the app. # By specifying the "latest" tag, it will also use whatever happens to be the # most recent version of that image when you build your Dockerfile. If # reproducability is important, consider using a versioned tag # (e.g., alpine:3.17.2) or SHA (e.g., alpine@sha256:c41ab5c992deb4fe7e5da09f67a8804a46bd0592bfdf0b1847dde0e0889d2bff). FROM alpine:latest AS final # Install any runtime dependencies that are needed to run your application. # Leverage a cache mount to /var/cache/apk/ to speed up subsequent builds. RUN --mount=type=cache,target=/var/cache/apk \ apk --update add \ ca-certificates \ tzdata \ && \ update-ca-certificates # Create a non-privileged user that the app will run under. # See https://docs.docker.com/go/dockerfile-user-best-practices/ ARG UID=10001 RUN adduser \ --disabled-password \ --gecos "" \ --home "/nonexistent" \ --shell "/sbin/nologin" \ --no-create-home \ --uid "${UID}" \ appuser USER appuser # Copy the executable from the "build" stage. COPY --from=build /bin/server /bin/ # Expose the port that the application listens on. EXPOSE 9000 # What the container should run when it is started. ENTRYPOINT \[ "/bin/server" \] 可以看到 Dockerfile 是一个常见的多阶段构建镜像流程。
...

 [post link to docker init 命令](https://jasminides.com/posts/docker_init_command/) [Go to Top (Alt + G)](https://jasminides.com/tags/init/#top "Go to Top (Alt + G)")

## gRPC Load Balancing
gRPC 中的负载均衡包括服务端负载均衡和客户端负载均衡，本文将介绍客户端负载均衡，gRPC 中的客户端负载均衡主要有 2 个部分:1) Name Resolver 2) Load Balancing Policy 接下来将依次介绍。
Name Resolver gRPC 中的默认 name-system 是 DNS , 同时各种客户端还提供了插件以使用自定义 name-system。gRPC Name Resolver 会根据 name-system 进行对应的解析，将用户提供的名称转换为对应的地址。
Load Balancing Policy gRPC 中内置了多种负载均衡策略，本文将介绍常见的几种负载均衡策略:1) pick\_first 2) round\_robin
pick\_first pick\_first 是默认的负载均衡策略，该策略从 Name Resolver 获得到服务器的地址列表，按顺序依次对每个服务器地址进行连接，直到连接成功，如果某个地址连接成功则所有的 RPC 请求都会发送到这个服务器地址。
round\_robin round\_robin 策略，该策略从 Name Resolver 获得到服务器的地址列表，依次将请求发送到每一个地址，例如第一个请求将发送到 backend1 ,第二个请求将发送到 backend2。
接下来分别使用这两种策略进行测试。
例子 我们先创建服务端，循环创建了 3 个服务端，分别使用 30051、30052、30053 端口。
package main import ( "context" "fmt" "log" "net" "sync" "google.golang.org/grpc" pb "github.com/overstarry/grpc-example/proto/echo" ) var ( addrs = \[\]string{":30051", ":30052",":30053"} ) type ecServer struct { pb.UnimplementedEchoServer addr string } func (s \*ecServer) UnaryEcho(ctx context.Context, req \*pb.EchoRequest) (\*pb.EchoResponse, error) { return &pb.EchoResponse{Message: fmt.Sprintf("%s (from %s)", req.Message, s.addr)}, nil } func startServer(addr string) { lis, err := net.Listen("tcp", addr) if err != nil { log.Fatalf("failed to listen: %v", err) } s := grpc.NewServer() pb.RegisterEchoServer(s, &ecServer{addr: addr}) log.Printf("serving on %s\\n", addr) if err := s.Serve(lis); err != nil { log.Fatalf("failed to serve: %v", err) } } func main() { var wg sync.WaitGroup for \_, addr := range addrs { wg.Add(1) go func(addr string) { defer wg.Done() startServer(addr) }(addr) } wg.Wait() } 接下来创建对应的客户端连接：
...

 [post link to gRPC 客户端负载均衡](https://jasminides.com/posts/grpc_client_load_balancing/)

前面的文章介绍了 gRPC 相关的功能，今天继续介绍 gRPC 的功能，本文将介绍 gRPC 的重试功能。
介绍 请求的重试是一个常见的功能，在我们日常的使用中，如果需要重试请求往往需要使用外部包进行实现，在 gRPC 中内置了重试了功能，不需要我们自己实现。
通过查阅 gRPC 的文档可以看到，gRPC 会根据开发者设定的策略进行失败 RPC 的重试，有两种策略 1) 重试策略：重试失败的 RPC 请求 2) hedging 策略：并行发生相同 RPC 请求。单个 RPC 请求可以选择两种重试策略中的一种，不能同时选择多种策略。
重试策略有以下参数可以使用：
maxAttempts: 必填 RPC 最大请求次数，包括原始请求 initialBackoff, maxBackoff, backoffMultiplier: 必填 决定下次重试前的延迟时间 random(0, min(initialBackoff\*backoffMultiplier\*\*(n-1), maxBackoff)) retryableStatusCodes: 必填 收到服务器非正常状态码时，根据 retryableStatusCodes 中的状态码列表决定是否重试请求 hedging 策略可以主动发送单个请求的多个副本，而无需等待响应。需要注意的是，此策略可能会导致后端多次执行，因此最好仅对可以多次执行不会有不利影响的请求开启此策略。有如下参数：
maxAttempts 必填 hedgingDelay 可选 nonFatalStatusCodes 可选 一个请求在没有收到成功响应时，经过 hedgingDelay 没收到响应 将继续发送请求，直至达到 maxAttempts 最大次数或请求成功。当收到成功响应时，所有未完成的其它请求将停止。本质上 hedging 策略可以看作在收到失败响应前重试请求。
使用 接下来讲解如何在 gRPC go 语言版本中配置使用重试功能。
服务端 服务端创建一个服务，只有当请求次数达到第三次时，才返回成功响应。
package main import ( "context" "flag" "fmt" "log" "net" "sync" "google.golang.org/grpc" "google.golang.org/grpc/codes" "google.golang.org/grpc/status" pb "github.com/overstarry/grpc-example/proto/echo" ) var port = flag.Int("port", 9000, "port number") type failingServer struct { pb.UnimplementedEchoServer mu sync.Mutex reqCounter uint reqModulo uint } func (s \*failingServer) maybeFailRequest() error { s.mu.Lock() defer s.mu.Unlock() s.reqCounter++ if (s.reqModulo > 0) && (s.reqCounter%s.reqModulo == 0) { return nil } return status.Errorf(codes.Unavailable, "maybeFailRequest: failing it") } func (s \*failingServer) UnaryEcho(ctx context.Context, req \*pb.EchoRequest) (\*pb.EchoResponse, error) { if err := s.maybeFailRequest(); err != nil { log.Println("request failed count:", s.reqCounter) return nil, err } log.Println("request succeeded count:", s.reqCounter) return &pb.EchoResponse{Message: req.Message}, nil } func main() { flag.Parse() address := fmt.Sprintf(":%v", \*port) lis, err := net.Listen("tcp", address) if err != nil { log.Fatalf("failed to listen: %v", err) } fmt.Println("listen on address", address) s := grpc.NewServer() failingservice := &failingServer{ reqCounter: 0, reqModulo: 3, } pb.RegisterEchoServer(s, failingservice) if err := s.Serve(lis); err != nil { log.Fatalf("failed to serve: %v", err) } } 客户端 客户端通过 WithDefaultServiceConfig 设置配置好重试功能
...

 [post link to gRPC 请求重试](https://jasminides.com/posts/grpc%E8%AF%B7%E6%B1%82%E9%87%8D%E8%AF%95/)

最近需要使用 apisix 来代理 gRPC 服务，本文记录一下 apisix 代理 gRPC 服务以及实践过程中遇到的一些问题。
准备 在接下来的步骤前，我们需要准备一个 gRPC 服务，我们使用 kratos 简单启动一个 gRPC 服务：
$ kratos new hellowrold $ cd helloworld $ kratos run 一个简单的 gRPC 服务就启动了，我们先直接请求 gRPC 服务看看，通过 postman 请求接口后，接口顺利返回相应的值。
接下来我们开始本篇的主要内容：apisix 代理服务。
apisix 代理 gRPC 服务 我们使用 apisix admin 接口创建 Route: upstream 的 scheme 指定为 grpc 或 grpcs,nodes 指定需要代理的服务地址。
curl http://127.0.0.1:9180/apisix/admin/routes/1 -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X PUT -d ' { "methods": \["POST", "GET"\], "uri": "/helloworld.v1.Greeter/SayHello", "upstream": { "scheme": "grpc", "type": "roundrobin", "nodes": { "127.0.0.1:9001": 1 } } }' ...

 [post link to apisix 代理 gRPC 服务](https://jasminides.com/posts/apisix_proxy_grpc_service/)

本文我来介绍 gRPC 中的中间件相关知识。
介绍 gRPC 中间件基于前面讲解的拦截器相关概念，它是一组拦截器、辅助、工具的集合，在我们使用 gRPC 开发应用时，往往会使用到各种中间件。它允许在服务端或客户端以拦截器链条形式应用多个中间件。因为拦截器经常用来实现一些通用的功能 ,如鉴权认证、日志、监控等，所以使用 gRPC 中间件来实现这些可重用功能是十分合适的。下面的代码就分别暂时服务端和客户端使用中间件的例子：
import "github.com/grpc-ecosystem/go-grpc-middleware" myServer := grpc.NewServer( grpc.StreamInterceptor(grpc\_middleware.ChainStreamServer( grpc\_ctxtags.StreamServerInterceptor(), grpc\_opentracing.StreamServerInterceptor(), grpc\_prometheus.StreamServerInterceptor, grpc\_zap.StreamServerInterceptor(zapLogger), grpc\_auth.StreamServerInterceptor(myAuthFunction), grpc\_recovery.StreamServerInterceptor(), )), grpc.UnaryInterceptor(grpc\_middleware.ChainUnaryServer( grpc\_ctxtags.UnaryServerInterceptor(), grpc\_opentracing.UnaryServerInterceptor(), grpc\_prometheus.UnaryServerInterceptor, grpc\_zap.UnaryServerInterceptor(zapLogger), grpc\_auth.UnaryServerInterceptor(myAuthFunction), grpc\_recovery.UnaryServerInterceptor(), )), ) import "github.com/grpc-ecosystem/go-grpc-middleware" clientConn, err = grpc.Dial( address, grpc.WithUnaryInterceptor(grpc\_middleware.ChainUnaryClient(monitoringClientUnary, retryUnary)), grpc.WithStreamInterceptor(grpc\_middleware.ChainStreamClient(monitoringClientStream, retryStream)), ) 常用的中间件 go-grpc-middleware 项目提供了一些常用的中间件：
认证 grpc\_auth - 一个可定制的（通过 AuthFunc）身份验证中间件 日志记录 grpc\_ctxtags - 将 Tag 地图添加到上下文的库，数据从请求正文填充 grpc\_zap - 将 zap 日志库集成到 gRPC 处理程序中。 grpc\_logrus - 将 logrus 日志库集成到 gRPC 处理程序中。 grpc\_kit - 将 go-kit/log 日志库集成到 gRPC 处理程序中。 grpc\_grpc\_logsettablegrpclog.LoggerV2 - 一个允许在运行时替换记录器的包装器（线程安全）。 监控 grpc\_prometheus - Prometheus 客户端和服务器端监控中间件 otgrpc - OpenTracing 客户端和服务器端拦截器 grpc\_opentracing - OpenTracing 客户端和服务器端拦截器，支持流式处理和处理程序返回的标签 otelgrpc - OpenTelemetry 客户端和服务器端拦截器 客户端中间件 grpc\_retry - 一个通用的 gRPC 响应代码重试机制，客户端中间件
...

 [post link to gRPC 中间件](https://jasminides.com/posts/grpc%E4%B8%AD%E9%97%B4%E4%BB%B6/)

前言 本文来简单介绍如何使用 wireshark 来获取 gRPC 请求。
wireshark 配置 在进行对 gRPC 请求抓包前，得来几个准备。
设置 proto 文件路径 依次打开 编辑 > 首选项 > Protocols > ProtoBuf, 点击如图选项，添加 proto 文件所在的路径。记得勾选右边的 “Load all files” 选项。
设置 TCP 消息解码 默认情况下，界面上显示的都是 TCP 数据包。依次点击菜单栏的 分析 -> 解码为… （或者右击随便一行）。
把 9000 (你的 gRPC 服务端端口) 端口的 TCP 消息解码成 HTTP2 协议信息。
开始抓包 现在开始捕获 gRPC 请求消息，为了避免其他无关的流量，在捕获选项设置筛选 tcp port 9000 只获得跟服务端相关的流量。
我们使用 postman 向服务端发送请求。回到 wireshark 界面，我们就可以看到许多流量，通过前面设置的解码，我们可以很方便的获得 gRPC 消息的具体内容。
小结 本文简单介绍了如何使用 wireshark 捕获 gRPC 请求流量。在使用 Wireshark 抓包时把未识别的 HTTP/2 协议手动设置为 HTTP/2，这样会方便很多。
...

 [post link to gRPC 请求抓包](https://jasminides.com/posts/grpc%E8%AF%B7%E6%B1%82%E6%8A%93%E5%8C%85/)

本文主要介绍 gRPC 的服务反射协议和相关的应用。
介绍 gRPC 服务反射协议 (server reflection) 是在 gRPC 服务端定义的一个服务，它能提供该服务器端上可公开使用的 gRPC 服务的信息，简单的来说，就是服务反射向客户端提供了服务端注册的服务的信息。因此客户端不需要预编译服务定义就能与服务端交互了。
客户端想要与服务端程序进行通信，必须要有所定义的服务信息，需要编译生产客户端存根，借助 gRPC 服务反射协议，我们就可以无需编译服务定义就能通信。
使用 该如何开启服务反射协议呢？很简单，只需要通过一行代码即可开启：reflection.Register()
package main import ( "context" "flag" "fmt" "log" "net" "google.golang.org/grpc" "google.golang.org/grpc/reflection" ecpb "google.golang.org/grpc/examples/features/proto/echo" hwpb "google.golang.org/grpc/examples/helloworld/helloworld" ) var port = flag.Int("port", 50051, "the port to serve on") // hwServer is used to implement helloworld.GreeterServer. type hwServer struct { hwpb.UnimplementedGreeterServer } // SayHello implements helloworld.GreeterServer func (s \*hwServer) SayHello(ctx context.Context, in \*hwpb.HelloRequest) (\*hwpb.HelloReply, error) { return &hwpb.HelloReply{Message: "Hello " + in.Name}, nil } type ecServer struct { ecpb.UnimplementedEchoServer } func (s \*ecServer) UnaryEcho(ctx context.Context, req \*ecpb.EchoRequest) (\*ecpb.EchoResponse, error) { return &ecpb.EchoResponse{Message: req.Message}, nil } func main() { flag.Parse() lis, err := net.Listen("tcp", fmt.Sprintf(":%d", \*port)) if err != nil { log.Fatalf("failed to listen: %v", err) } fmt.Printf("server listening at %v\\n", lis.Addr()) s := grpc.NewServer() // Register Greeter on the server. hwpb.RegisterGreeterServer(s, &hwServer{}) // Register RouteGuide on the same server. ecpb.RegisterEchoServer(s, &ecServer{}) // Register reflection service on gRPC server. reflection.Register(s) if err := s.Serve(lis); err != nil { log.Fatalf("failed to serve: %v", err) } } 服务端开启服务反射协议后，就可以通过 gRPC CLI 工具来检查服务端了。这里就不多介绍了，接下来我们来看看服务反射协议在 kratos 中的使用。
...

 [post link to gRPC 服务反射协议](https://jasminides.com/posts/grpc_server_reflection/)

简介 gRPC 健康探针 grpc-health-probe 是社区提供的一个工具，用来检查 gRPC 服务的健康状态，此工具 是通过 gRPC 健康检查协议公开服务的状态。
使用 我在本地使用 kratos 创建一个使用 9000 端口的 gRPC 的服务。通过 grpc-health-probe 可以检查服务的健康状态。
grpc-health-probe -addr=localhost:9000 status: SERVING 可以看到此服务目前是健康的，不健康的服务将以非零退出代码退出。
grpc\_health\_probe -addr=localhost:9000 -connect-timeout 250ms -rpc-timeout 100ms failed to connect service at "localhost:9000": context deadline exceeded exit status 2 grpc\_health\_probe 发送了一个对 /grpc.health.v1.Health/Check 的 RPC 请求。如果已 SERVING 状态作为响应，就会正常成功退出，否则会给出一个非零的退出。
Kubernetes 使用 grpc\_health\_probe 可用于 Kubernetes 对 Pod 中运行的 gRPC 服务器进行健康检查。建议您使用 Kubernetes exec 探针并为您的 gRPC 服务器 pod 定义活跃度和/或就绪性检查。
您可以将静态编译 grpc\_health\_probe 的内容捆绑到您的容器映像中。
...

 [post link to gRPC 健康探针](https://jasminides.com/posts/grpc%E5%81%A5%E5%BA%B7%E6%8E%A2%E9%92%88/)

本篇文章我来介绍 gRPC 中的健康检查相关的知识。
简介 服务的健康检测一般是指的是检测服务是否正常运行：
是否存在，因为程序逻辑错误或者 OOM 等进程不存在； 存在是否可以正常的响应请求，尽管进程存在但可能因为请求量过大或者程序逻辑错误，导致服务 hang 住，无法正常对外请求。 gRPC 定义了一个健康检查协议，它允许使用了 gRPC 服务暴露服务器的状态，这样服务的消费者就能获得服务的健康状态。服务器的健康状态是由服务器是否响应非健康状态来确定的。 当服务器还没准备好处理 rpc 请求或者根本没有响应健康探针的请求时，就会发生这种情况。
健康服务定义 gRPC 健康检查协议基于 gRPC 定义了 API。下面就是服务定义：
syntax = "proto3"; package grpc.health.v1; message HealthCheckRequest { string service = 1; } message HealthCheckResponse { enum ServingStatus { UNKNOWN = 0; SERVING = 1; NOT\_SERVING = 2; } ServingStatus status = 1; } service Health { rpc Check(HealthCheckRequest) returns (HealthCheckResponse); rpc Watch(HealthCheckRequest) returns (stream HealthCheckResponse); } 客户端应该调用 Check 服务来判断服务是否正常运行，并且设置 deadline。客户端可以设置需要查询的服务名称，来返回对应的服务是否正常。
服务器应手动注册所有的服务并单个设置状态，包括空服务名称及其状态。对于收到的每一个请求，从注册表中查询服务的状态并返回。如果未找到，返回 NOT\_FOUND 状态。服务器也可以根据实际的业务逻辑提供更为复杂的状态返回。
...

 [post link to GRPC 健康检查](https://jasminides.com/posts/grpc%E5%81%A5%E5%BA%B7%E6%A3%80%E6%9F%A5/)

从本篇开始，我将介绍加强 gRPC 的安全性的一系列措施。本篇介绍使用 TLS 加密 gRPC 通信的第一篇文章：gRPC 单向安全连接。
TLS 协议介绍 传输层安全性协议（英语：Transport Layer Security，缩写作 TLS），及其前身安全套接层（Secure Sockets Layer，缩写作 SSL）是一种安全协议，目的是为互联网通信提供安全及数据完整性保障。网景公司（Netscape）在 1994 年推出首版网页浏览器，网景导航者时，推出 HTTPS 协议，以 SSL 进行加密，这是 SSL 的起源。IETF 将 SSL 进行标准化，1999 年公布第一版 TLS 标准文件。随后又公布 RFC 5246（2008 年 8 月）与 RFC 6176（2011 年 3 月）。在浏览器、邮箱、即时通信、VoIP、网络传真等应用程序中，广泛支持这个协议。主要的网站，如 Google、Facebook 等也以这个协议来创建安全连线，发送数据。目前已成为互联网上保密通信的工业标准。
SSL 包含记录层（Record Layer）和传输层，记录层协议确定传输层数据的封装格式。传输层安全协议使用 X.509 认证，之后利用非对称加密演算来对通信方做身份认证，之后交换对称密钥作为会谈密钥（Session key）。这个会谈密钥是用来将通信两方交换的数据做加密，保证两个应用间通信的保密性和可靠性，使客户与服务器应用之间的通信不被攻击者窃听。
单向安全连接 通过安全的连接进行传输数据非常重要，那么如何在 gRPC 中使用 TLS 保护 gRPC 通信呢？TLS 认证机制集成在了 gRPC 库中，这使得 gRPC 可以很方便使用 TLS 进行安全连接。 客户端和服务端之间的安全传输可以采用单向或双向的方式来实现。本文主要介绍 单向安全连接。
在单向安全连接中，只有客户端会校验服务端，以确保它所接收的数据来自预期的服务器，在建立连接时，服务端会与客户端共享其公开证书，客户端会校验收到的证书。这是通过证书授权中心完成的。证书校验完成后，客户端会使用密钥加密数据。
要启用 TLS，需要证书和密钥 (xx.key,xx.pem/xx.crt),前者是用于签名和扔着公钥，后者用于分发自签名 X.509 公钥。证书和密钥的生成这里就不过多介绍了，需要的可以自行了解。
...

 [post link to GRPC 单向安全连接](https://jasminides.com/posts/grpc%E5%8D%95%E5%90%91%E5%AE%89%E5%85%A8%E8%BF%9E%E6%8E%A5/)

今天来讲一讲 gRPC 的多路复用，gRPC 的多路复用是指 一个 gRPC 服务器端可以运行多个 gRPC 服务，也允许多个客户端存根使用同一个 gRPC 客户端连接。
我们继续沿用前面的代码来讲解如何使用多路复用。
多个 gRPC 服务共享同一个服务器端 假如在订单服务中，为了管理的需求，需要在同一个服务端运行另一个 RPC 服务，这样客户端就能重用同一个连接，这样就可以按需调用相应的服务。通过相应的服务器端注册函数，可以使多个服务注册在同一个服务器端。
具体代码如下：
func main() { initSampleData() lis, err := net.Listen("tcp", port) if err != nil { log.Fatalf("failed to isten: %v", err) } s := grpc.NewServer(grpc.UnaryInterceptor(orderUnaryServerInterceptor)) ordermgt\_pb.RegisterOrderManagementServer(s, &orderMgtServer{}) user\_pb.RegisterUserManagementServer(s, &userMgtServer{}) if err := s.Serve(lis); err != nil { log.Fatalf("failed to serve: %v", err) } } 这样就是多个 gRPC 服务共享同一个服务端连接，这样就可以按需调用相应的服务。同理，通过客户端，可以在两个 gRPC 客户端存根间共享相同的 gRPC 客户端连接。
两个 gRPC 客户端存根共享同一个客户端连接 如代码所示，两个 gRPC 服务在同一个 gRPC 服务器端运行，所以可以创建一个 gRPC 连接，并在两个服务创建 gRPC 客户端实例时使用这个连接。
func main() { conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock()) if err != nil { log.Fatalf("did not connect: %v", err) } defer conn.Close() client := pb.NewOrderManagementClient(conn) ctx, cancel := context.WithTimeout(context.Background(), time.Second\*5) defer cancel() heclien := hwpb.NewGreetingClient(conn) } 小结 在我们的日常使用中，通常不会出现两个服务间共享同一个服务器端连接的情况。
...

 [post link to GRPC 多路复用](https://jasminides.com/posts/grpc%E5%A4%9A%E8%B7%AF%E5%A4%8D%E7%94%A8/) [Go to Top (Alt + G)](https://jasminides.com/tags/grpc/#top "Go to Top (Alt + G)")

## gRPC Load Balancing
目录

- [Name Resolver](https://jasminides.com/posts/grpc_client_load_balancing/#name-resolver)
- [Load Balancing Policy](https://jasminides.com/posts/grpc_client_load_balancing/#load-balancing-policy)
  - [pick\_first](https://jasminides.com/posts/grpc_client_load_balancing/#pick_first)
  - [round\_robin](https://jasminides.com/posts/grpc_client_load_balancing/#round_robin)
  - [例子](https://jasminides.com/posts/grpc_client_load_balancing/#%e4%be%8b%e5%ad%90)
- [参考](https://jasminides.com/posts/grpc_client_load_balancing/#%e5%8f%82%e8%80%83)

gRPC 中的负载均衡包括服务端负载均衡和客户端负载均衡，本文将介绍客户端负载均衡，gRPC 中的客户端负载均衡主要有 2 个部分:1) Name Resolver 2) Load Balancing Policy 接下来将依次介绍。

## Name Resolver

gRPC 中的默认 name-system 是 DNS , 同时各种客户端还提供了插件以使用自定义 name-system。gRPC Name Resolver 会根据 name-system 进行对应的解析，将用户提供的名称转换为对应的地址。

## Load Balancing Policy

gRPC 中内置了多种负载均衡策略，本文将介绍常见的几种负载均衡策略:1) pick\_first 2) round\_robin

### pick\_first

pick\_first 是默认的负载均衡策略，该策略从 Name Resolver 获得到服务器的地址列表，按顺序依次对每个服务器地址进行连接，直到连接成功，如果某个地址连接成功则所有的 RPC 请求都会发送到这个服务器地址。

### round\_robin

round\_robin 策略，该策略从 Name Resolver 获得到服务器的地址列表，依次将请求发送到每一个地址，例如第一个请求将发送到 backend1 ,第二个请求将发送到 backend2。

接下来分别使用这两种策略进行测试。

### 例子

我们先创建服务端，循环创建了 3 个服务端，分别使用 30051、30052、30053 端口。

```go
package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"sync"

	"google.golang.org/grpc"

	pb "github.com/overstarry/grpc-example/proto/echo"
)

var (
	addrs = []string{":30051", ":30052",":30053"}
)

type ecServer struct {
	pb.UnimplementedEchoServer
	addr string
}

func (s *ecServer) UnaryEcho(ctx context.Context, req *pb.EchoRequest) (*pb.EchoResponse, error) {
	return &pb.EchoResponse{Message: fmt.Sprintf("%s (from %s)", req.Message, s.addr)}, nil
}

func startServer(addr string) {
	lis, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterEchoServer(s, &ecServer{addr: addr})
	log.Printf("serving on %s\n", addr)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

func main() {
	var wg sync.WaitGroup
	for _, addr := range addrs {
		wg.Add(1)
		go func(addr string) {
			defer wg.Done()
			startServer(addr)
		}(addr)
	}
	wg.Wait()
}

```

复制

接下来创建对应的客户端连接：

```go
package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	pb "github.com/overstarry/grpc-example/proto/echo"
	"google.golang.org/grpc/resolver"
)

const (
	exampleScheme      = "example"
	exampleServiceName = "lb.overstarry.grpc.io"
)

var addrs = []string{"localhost:30051", "localhost:30052", "localhost:30053"}

func callUnaryEcho(c pb.EchoClient, message string) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	r, err := c.UnaryEcho(ctx, &pb.EchoRequest{Message: message})
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	fmt.Println(r.Message)
}

func makeRPCs(cc *grpc.ClientConn, n int) {
	hwc := pb.NewEchoClient(cc)
	for i := 0; i < n; i++ {
		callUnaryEcho(hwc, "this is examples/load_balancing")
	}
}

func main() {
	pickfirstConn, err := grpc.Dial(
		fmt.Sprintf("%s:///%s", exampleScheme, exampleServiceName),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer pickfirstConn.Close()

	makeRPCs(pickfirstConn, 10)

	fmt.Println()

	roundrobinConn, err := grpc.Dial(
		fmt.Sprintf("%s:///%s", exampleScheme, exampleServiceName),
		grpc.WithDefaultServiceConfig(`{"loadBalancingConfig": [{"round_robin":{}}]}`), // This sets the initial balancing policy.
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer roundrobinConn.Close()

	makeRPCs(roundrobinConn, 10)
}

type exampleResolverBuilder struct{}

func (*exampleResolverBuilder) Build(target resolver.Target, cc resolver.ClientConn, opts resolver.BuildOptions) (resolver.Resolver, error) {
	r := &exampleResolver{
		target: target,
		cc:     cc,
		addrsStore: map[string][]string{
			exampleServiceName: addrs,
		},
	}
	r.start()
	return r, nil
}
func (*exampleResolverBuilder) Scheme() string { return exampleScheme }

type exampleResolver struct {
	target     resolver.Target
	cc         resolver.ClientConn
	addrsStore map[string][]string
}

func (r *exampleResolver) start() {
	addrStrs := r.addrsStore[r.target.Endpoint()]
	addrs := make([]resolver.Address, len(addrStrs))
	for i, s := range addrStrs {
		addrs[i] = resolver.Address{Addr: s}
	}
	r.cc.UpdateState(resolver.State{Addresses: addrs})
}
func (*exampleResolver) ResolveNow(o resolver.ResolveNowOptions) {}
func (*exampleResolver) Close()                                  {}

func init() {
	resolver.Register(&exampleResolverBuilder{})
}

```

复制

可以看到通过 grpc.WithDefaultServiceConfig 可以指定使用的负载均衡策略，由于测试的需要，我们还创建了自定义的 Name Resolver 用来测试使用。

运行代码：

```console
2024/03/30 17:37:33 pick_first
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30051)

2024/03/30 17:37:33 round_robin
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30052)
this is examples/load_balancing (from :30053)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30052)
this is examples/load_balancing (from :30053)
this is examples/load_balancing (from :30051)
this is examples/load_balancing (from :30052)
this is examples/load_balancing (from :30053)

```

复制

可以看到结果与相应的策略效果一致。

## 参考

- [https://github.com/grpc/grpc/blob/master/doc/naming.md](https://github.com/grpc/grpc/blob/master/doc/naming.md)
- [https://github.com/grpc/grpc/blob/master/doc/load-balancing.md](https://github.com/grpc/grpc/blob/master/doc/load-balancing.md)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fgrpc_client_load_balancing%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/grpc_client_load_balancing/#top "Go to Top (Alt + G)")

## gRPC Load Balancing
gRPC 中的负载均衡包括服务端负载均衡和客户端负载均衡，本文将介绍客户端负载均衡，gRPC 中的客户端负载均衡主要有 2 个部分:1) Name Resolver 2) Load Balancing Policy 接下来将依次介绍。
Name Resolver gRPC 中的默认 name-system 是 DNS , 同时各种客户端还提供了插件以使用自定义 name-system。gRPC Name Resolver 会根据 name-system 进行对应的解析，将用户提供的名称转换为对应的地址。
Load Balancing Policy gRPC 中内置了多种负载均衡策略，本文将介绍常见的几种负载均衡策略:1) pick\_first 2) round\_robin
pick\_first pick\_first 是默认的负载均衡策略，该策略从 Name Resolver 获得到服务器的地址列表，按顺序依次对每个服务器地址进行连接，直到连接成功，如果某个地址连接成功则所有的 RPC 请求都会发送到这个服务器地址。
round\_robin round\_robin 策略，该策略从 Name Resolver 获得到服务器的地址列表，依次将请求发送到每一个地址，例如第一个请求将发送到 backend1 ,第二个请求将发送到 backend2。
接下来分别使用这两种策略进行测试。
例子 我们先创建服务端，循环创建了 3 个服务端，分别使用 30051、30052、30053 端口。
package main import ( "context" "fmt" "log" "net" "sync" "google.golang.org/grpc" pb "github.com/overstarry/grpc-example/proto/echo" ) var ( addrs = \[\]string{":30051", ":30052",":30053"} ) type ecServer struct { pb.UnimplementedEchoServer addr string } func (s \*ecServer) UnaryEcho(ctx context.Context, req \*pb.EchoRequest) (\*pb.EchoResponse, error) { return &pb.EchoResponse{Message: fmt.Sprintf("%s (from %s)", req.Message, s.addr)}, nil } func startServer(addr string) { lis, err := net.Listen("tcp", addr) if err != nil { log.Fatalf("failed to listen: %v", err) } s := grpc.NewServer() pb.RegisterEchoServer(s, &ecServer{addr: addr}) log.Printf("serving on %s\\n", addr) if err := s.Serve(lis); err != nil { log.Fatalf("failed to serve: %v", err) } } func main() { var wg sync.WaitGroup for \_, addr := range addrs { wg.Add(1) go func(addr string) { defer wg.Done() startServer(addr) }(addr) } wg.Wait() } 接下来创建对应的客户端连接：
...

 [post link to gRPC 客户端负载均衡](https://jasminides.com/posts/grpc_client_load_balancing/) [Go to Top (Alt + G)](https://jasminides.com/tags/load_balancing/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fload_balancing%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801924175&bpp=2&bdt=140&idt=102&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=3561147938296&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95355300&oid=2&pvsid=4021141621022483&tmod=1182028619&uas=0&nvt=1&fsapi=1&fc=1920&brdim=90%2C90%2C90%2C90%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=127)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## gRPC Client Load Balancing
gRPC 中的负载均衡包括服务端负载均衡和客户端负载均衡，本文将介绍客户端负载均衡，gRPC 中的客户端负载均衡主要有 2 个部分:1) Name Resolver 2) Load Balancing Policy 接下来将依次介绍。
Name Resolver gRPC 中的默认 name-system 是 DNS , 同时各种客户端还提供了插件以使用自定义 name-system。gRPC Name Resolver 会根据 name-system 进行对应的解析，将用户提供的名称转换为对应的地址。
Load Balancing Policy gRPC 中内置了多种负载均衡策略，本文将介绍常见的几种负载均衡策略:1) pick\_first 2) round\_robin
pick\_first pick\_first 是默认的负载均衡策略，该策略从 Name Resolver 获得到服务器的地址列表，按顺序依次对每个服务器地址进行连接，直到连接成功，如果某个地址连接成功则所有的 RPC 请求都会发送到这个服务器地址。
round\_robin round\_robin 策略，该策略从 Name Resolver 获得到服务器的地址列表，依次将请求发送到每一个地址，例如第一个请求将发送到 backend1 ,第二个请求将发送到 backend2。
接下来分别使用这两种策略进行测试。
例子 我们先创建服务端，循环创建了 3 个服务端，分别使用 30051、30052、30053 端口。
package main import ( "context" "fmt" "log" "net" "sync" "google.golang.org/grpc" pb "github.com/overstarry/grpc-example/proto/echo" ) var ( addrs = \[\]string{":30051", ":30052",":30053"} ) type ecServer struct { pb.UnimplementedEchoServer addr string } func (s \*ecServer) UnaryEcho(ctx context.Context, req \*pb.EchoRequest) (\*pb.EchoResponse, error) { return &pb.EchoResponse{Message: fmt.Sprintf("%s (from %s)", req.Message, s.addr)}, nil } func startServer(addr string) { lis, err := net.Listen("tcp", addr) if err != nil { log.Fatalf("failed to listen: %v", err) } s := grpc.NewServer() pb.RegisterEchoServer(s, &ecServer{addr: addr}) log.Printf("serving on %s\\n", addr) if err := s.Serve(lis); err != nil { log.Fatalf("failed to serve: %v", err) } } func main() { var wg sync.WaitGroup for \_, addr := range addrs { wg.Add(1) go func(addr string) { defer wg.Done() startServer(addr) }(addr) } wg.Wait() } 接下来创建对应的客户端连接：
...

 [post link to gRPC 客户端负载均衡](https://jasminides.com/posts/grpc_client_load_balancing/) [Go to Top (Alt + G)](https://jasminides.com/tags/%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1/#top "Go to Top (Alt + G)")

## gRPC Retry Functionality
目录

- [介绍](https://jasminides.com/posts/grpc%E8%AF%B7%E6%B1%82%E9%87%8D%E8%AF%95/#%e4%bb%8b%e7%bb%8d)
- [使用](https://jasminides.com/posts/grpc%E8%AF%B7%E6%B1%82%E9%87%8D%E8%AF%95/#%e4%bd%bf%e7%94%a8)
  - [服务端](https://jasminides.com/posts/grpc%E8%AF%B7%E6%B1%82%E9%87%8D%E8%AF%95/#%e6%9c%8d%e5%8a%a1%e7%ab%af)
  - [客户端](https://jasminides.com/posts/grpc%E8%AF%B7%E6%B1%82%E9%87%8D%E8%AF%95/#%e5%ae%a2%e6%88%b7%e7%ab%af)
- [小结](https://jasminides.com/posts/grpc%E8%AF%B7%E6%B1%82%E9%87%8D%E8%AF%95/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/grpc%E8%AF%B7%E6%B1%82%E9%87%8D%E8%AF%95/#%e5%8f%82%e8%80%83)

前面的文章介绍了 gRPC 相关的功能，今天继续介绍 gRPC 的功能，本文将介绍 gRPC 的重试功能。

## 介绍

请求的重试是一个常见的功能，在我们日常的使用中，如果需要重试请求往往需要使用外部包进行实现，在 gRPC 中内置了重试了功能，不需要我们自己实现。

通过查阅 gRPC 的文档可以看到，gRPC 会根据开发者设定的策略进行失败 RPC 的重试，有两种策略 1) 重试策略：重试失败的 RPC 请求 2) hedging 策略：并行发生相同 RPC 请求。单个 RPC 请求可以选择两种重试策略中的一种，不能同时选择多种策略。

重试策略有以下参数可以使用：

- maxAttempts: 必填 RPC 最大请求次数，包括原始请求
- initialBackoff, maxBackoff, backoffMultiplier: 必填 决定下次重试前的延迟时间 random(0, min(initialBackoff\*backoffMultiplier\*\*(n-1), maxBackoff))
- retryableStatusCodes: 必填 收到服务器非正常状态码时，根据 retryableStatusCodes 中的状态码列表决定是否重试请求

hedging 策略可以主动发送单个请求的多个副本，而无需等待响应。需要注意的是，此策略可能会导致后端多次执行，因此最好仅对可以多次执行不会有不利影响的请求开启此策略。有如下参数：

- maxAttempts 必填
- hedgingDelay 可选
- nonFatalStatusCodes 可选

一个请求在没有收到成功响应时，经过 hedgingDelay 没收到响应 将继续发送请求，直至达到 maxAttempts 最大次数或请求成功。当收到成功响应时，所有未完成的其它请求将停止。本质上 hedging 策略可以看作在收到失败响应前重试请求。

## 使用

接下来讲解如何在 gRPC go 语言版本中配置使用重试功能。

### 服务端

服务端创建一个服务，只有当请求次数达到第三次时，才返回成功响应。

```go
package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"
	"sync"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	pb "github.com/overstarry/grpc-example/proto/echo"
)

var port = flag.Int("port", 9000, "port number")

type failingServer struct {
	pb.UnimplementedEchoServer
	mu sync.Mutex

	reqCounter uint
	reqModulo  uint
}

func (s *failingServer) maybeFailRequest() error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.reqCounter++
	if (s.reqModulo > 0) && (s.reqCounter%s.reqModulo == 0) {
		return nil
	}

	return status.Errorf(codes.Unavailable, "maybeFailRequest: failing it")
}

func (s *failingServer) UnaryEcho(ctx context.Context, req *pb.EchoRequest) (*pb.EchoResponse, error) {
	if err := s.maybeFailRequest(); err != nil {
		log.Println("request failed count:", s.reqCounter)
		return nil, err
	}

	log.Println("request succeeded count:", s.reqCounter)
	return &pb.EchoResponse{Message: req.Message}, nil
}

func main() {
	flag.Parse()

	address := fmt.Sprintf(":%v", *port)
	lis, err := net.Listen("tcp", address)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	fmt.Println("listen on address", address)

	s := grpc.NewServer()


	failingservice := &failingServer{
		reqCounter: 0,
		reqModulo:  3,
	}

	pb.RegisterEchoServer(s, failingservice)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

```

复制

### 客户端

客户端通过 WithDefaultServiceConfig 设置配置好重试功能

```go
package main

import (
	"context"
	"flag"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	pb "github.com/overstarry/grpc-example/proto/echo"
)

var (
	addr = flag.String("addr", "127.0.0.1:9000", "the address to connect to")
	// see https://github.com/grpc/grpc/blob/master/doc/service_config.md to know more about service config
	retryPolicy = `{
		"methodConfig": [{\
		  "name": [{"service": "grpc.examples.echo.Echo"}],\
		  "waitForReady": true,\
		  "retryPolicy": {\
			  "MaxAttempts": 4,\
			  "InitialBackoff": ".01s",\
			  "MaxBackoff": ".01s",\
			  "BackoffMultiplier": 1.0,\
			  "RetryableStatusCodes": [ "UNAVAILABLE" ]\
		  }\
		}]}`
)

func retryDial() (*grpc.ClientConn, error) {
	return grpc.Dial(*addr, grpc.WithTransportCredentials(insecure.NewCredentials()), grpc.WithDefaultServiceConfig(retryPolicy))
}

func main() {
	flag.Parse()

	// Set up a connection to the server.
	conn, err := retryDial()
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer func() {
		if e := conn.Close(); e != nil {
			log.Printf("failed to close connection: %s", e)
		}
	}()

	c := pb.NewEchoClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	reply, err := c.UnaryEcho(ctx, &pb.EchoRequest{Message: "Try and Success"})
	if err != nil {
		log.Fatalf("UnaryEcho error: %v", err)
	}
	log.Printf("UnaryEcho reply: %v", reply)
}

```

复制

接下来先启动服务端，再启动客户端，可以看到相应的日志：

```console
2024/03/23 23:10:03 request failed count: 1
2024/03/23 23:10:03 request failed count: 2
2024/03/23 23:10:03 request succeeded count: 3

```

复制

在客户端代码中我们可以看到相关的配置代码：

```go
retryPolicy = `{
		"methodConfig": [{\
		  "name": [{"service": "grpc.examples.echo.Echo"}],\
		  "waitForReady": true,\
		  "retryPolicy": {\
			  "MaxAttempts": 4,\
			  "InitialBackoff": ".01s",\
			  "MaxBackoff": ".01s",\
			  "BackoffMultiplier": 1.0,\
			  "RetryableStatusCodes": [ "UNAVAILABLE" ]\
		  }\
		}]}`

```

复制

retryPolicy 就是上文讲述的重试策略配置，name 表示对哪些 RPC 请求开启重试。

## 小结

本文简单介绍了 gRPC 的重试功能及 go 语言如何实现重试功能，本文的相关代码可以在 [https://github.com/overstarry/grpc-example](https://github.com/overstarry/grpc-example) 看到。

## 参考

- [https://github.com/grpc/proposal/blob/master/A6-client-retries.md](https://github.com/grpc/proposal/blob/master/A6-client-retries.md)
- [https://github.com/grpc/grpc-go/tree/master/examples/features/retry](https://github.com/grpc/grpc-go/tree/master/examples/features/retry)
- [https://github.com/grpc/grpc/blob/master/doc/service\_config.md](https://github.com/grpc/grpc/blob/master/doc/service_config.md)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fgrpc%25E8%25AF%25B7%25E6%25B1%2582%25E9%2587%258D%25E8%25AF%2595%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/grpc%E8%AF%B7%E6%B1%82%E9%87%8D%E8%AF%95/#top "Go to Top (Alt + G)")

## gRPC Retry Features
前面的文章介绍了 gRPC 相关的功能，今天继续介绍 gRPC 的功能，本文将介绍 gRPC 的重试功能。
介绍 请求的重试是一个常见的功能，在我们日常的使用中，如果需要重试请求往往需要使用外部包进行实现，在 gRPC 中内置了重试了功能，不需要我们自己实现。
通过查阅 gRPC 的文档可以看到，gRPC 会根据开发者设定的策略进行失败 RPC 的重试，有两种策略 1) 重试策略：重试失败的 RPC 请求 2) hedging 策略：并行发生相同 RPC 请求。单个 RPC 请求可以选择两种重试策略中的一种，不能同时选择多种策略。
重试策略有以下参数可以使用：
maxAttempts: 必填 RPC 最大请求次数，包括原始请求 initialBackoff, maxBackoff, backoffMultiplier: 必填 决定下次重试前的延迟时间 random(0, min(initialBackoff\*backoffMultiplier\*\*(n-1), maxBackoff)) retryableStatusCodes: 必填 收到服务器非正常状态码时，根据 retryableStatusCodes 中的状态码列表决定是否重试请求 hedging 策略可以主动发送单个请求的多个副本，而无需等待响应。需要注意的是，此策略可能会导致后端多次执行，因此最好仅对可以多次执行不会有不利影响的请求开启此策略。有如下参数：
maxAttempts 必填 hedgingDelay 可选 nonFatalStatusCodes 可选 一个请求在没有收到成功响应时，经过 hedgingDelay 没收到响应 将继续发送请求，直至达到 maxAttempts 最大次数或请求成功。当收到成功响应时，所有未完成的其它请求将停止。本质上 hedging 策略可以看作在收到失败响应前重试请求。
使用 接下来讲解如何在 gRPC go 语言版本中配置使用重试功能。
服务端 服务端创建一个服务，只有当请求次数达到第三次时，才返回成功响应。
package main import ( "context" "flag" "fmt" "log" "net" "sync" "google.golang.org/grpc" "google.golang.org/grpc/codes" "google.golang.org/grpc/status" pb "github.com/overstarry/grpc-example/proto/echo" ) var port = flag.Int("port", 9000, "port number") type failingServer struct { pb.UnimplementedEchoServer mu sync.Mutex reqCounter uint reqModulo uint } func (s \*failingServer) maybeFailRequest() error { s.mu.Lock() defer s.mu.Unlock() s.reqCounter++ if (s.reqModulo > 0) && (s.reqCounter%s.reqModulo == 0) { return nil } return status.Errorf(codes.Unavailable, "maybeFailRequest: failing it") } func (s \*failingServer) UnaryEcho(ctx context.Context, req \*pb.EchoRequest) (\*pb.EchoResponse, error) { if err := s.maybeFailRequest(); err != nil { log.Println("request failed count:", s.reqCounter) return nil, err } log.Println("request succeeded count:", s.reqCounter) return &pb.EchoResponse{Message: req.Message}, nil } func main() { flag.Parse() address := fmt.Sprintf(":%v", \*port) lis, err := net.Listen("tcp", address) if err != nil { log.Fatalf("failed to listen: %v", err) } fmt.Println("listen on address", address) s := grpc.NewServer() failingservice := &failingServer{ reqCounter: 0, reqModulo: 3, } pb.RegisterEchoServer(s, failingservice) if err := s.Serve(lis); err != nil { log.Fatalf("failed to serve: %v", err) } } 客户端 客户端通过 WithDefaultServiceConfig 设置配置好重试功能
...

 [post link to gRPC 请求重试](https://jasminides.com/posts/grpc%E8%AF%B7%E6%B1%82%E9%87%8D%E8%AF%95/) [Go to Top (Alt + G)](https://jasminides.com/tags/retry/#top "Go to Top (Alt + G)")

## Aliyun Database Connection Issues
问题 最近收到了阿里云云数据库的报警信息，提示数据库连接数过高，通过监控可以看到，数据库的连接数升高了 50%,其它指标保持正常。
分析及解决 通过阿里云后台的一键诊断中的会话管理可以看到占用大量连接的 ip 地址，可以看到 100.104.205.90、100.104.205.83 和 100.104.205.6 这三个 ip 占用了大量连接，可以看到并没有 sql 请求，只是单纯的保持数据库连接，通过查看阿里云文档和询问客服，可以得知这个 ip 地址是阿里云 dms 服务的地址，。
找到原因后就好解决了，可以使用SELECT pg\_terminate\_backend(pid)语句释放数据库连接，使用语句释放与这三个 ip 相关的数据库连接:select pg\_terminate\_backend(pid) from pg\_stat\_activity where client\_addr in ('100.104.205.90','100.104.205.83') ,过了一会数据库连接恢复正常了。
小结 本文通过阿里云数据库连接过高的问题，分析遇到此类问题时如何排查并解决。
参考 https://help.aliyun.com/zh/dms/configure-an-ip-address-whitelist

 [post link to 阿里云 dms 占用数据库连接问题及解决](https://jasminides.com/posts/alliyunrdserr/) [Go to Top (Alt + G)](https://jasminides.com/tags/aliyun/#top "Go to Top (Alt + G)")

## Alibaba Cloud DMS Connection Issues
问题 最近收到了阿里云云数据库的报警信息，提示数据库连接数过高，通过监控可以看到，数据库的连接数升高了 50%,其它指标保持正常。
分析及解决 通过阿里云后台的一键诊断中的会话管理可以看到占用大量连接的 ip 地址，可以看到 100.104.205.90、100.104.205.83 和 100.104.205.6 这三个 ip 占用了大量连接，可以看到并没有 sql 请求，只是单纯的保持数据库连接，通过查看阿里云文档和询问客服，可以得知这个 ip 地址是阿里云 dms 服务的地址，。
找到原因后就好解决了，可以使用SELECT pg\_terminate\_backend(pid)语句释放数据库连接，使用语句释放与这三个 ip 相关的数据库连接:select pg\_terminate\_backend(pid) from pg\_stat\_activity where client\_addr in ('100.104.205.90','100.104.205.83') ,过了一会数据库连接恢复正常了。
小结 本文通过阿里云数据库连接过高的问题，分析遇到此类问题时如何排查并解决。
参考 https://help.aliyun.com/zh/dms/configure-an-ip-address-whitelist

 [post link to 阿里云 dms 占用数据库连接问题及解决](https://jasminides.com/posts/alliyunrdserr/) [Go to Top (Alt + G)](https://jasminides.com/tags/dms/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fdms%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801929269&bpp=3&bdt=159&idt=91&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=6658018440377&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C42532523%2C95355905%2C95354564%2C31091145%2C95355300&oid=2&pvsid=2888480901097374&tmod=980206765&uas=0&nvt=1&fsapi=1&fc=1920&brdim=200%2C200%2C200%2C200%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=118)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Aliyun Database Connection Issues
目录

- [问题](https://jasminides.com/posts/alliyunrdserr/#%e9%97%ae%e9%a2%98)
- [分析及解决](https://jasminides.com/posts/alliyunrdserr/#%e5%88%86%e6%9e%90%e5%8f%8a%e8%a7%a3%e5%86%b3)
- [小结](https://jasminides.com/posts/alliyunrdserr/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/alliyunrdserr/#%e5%8f%82%e8%80%83)

## 问题

最近收到了阿里云云数据库的报警信息，提示数据库连接数过高，通过监控可以看到，数据库的连接数升高了 50%,其它指标保持正常。

## 分析及解决

通过阿里云后台的一键诊断中的会话管理可以看到占用大量连接的 ip 地址，可以看到 100.104.205.90、100.104.205.83
和 100.104.205.6 这三个 ip 占用了大量连接，可以看到并没有 sql 请求，只是单纯的保持数据库连接，通过查看阿里云文档和询问客服，可以得知这个 ip 地址是阿里云 dms 服务的地址，。

![img.png](https://jasminides.com/img/aliyundms/img.png)![img_1.png](https://jasminides.com/img/aliyundms/img_1.png)![img_2.png](https://jasminides.com/img/aliyundms/img_2.png)

找到原因后就好解决了，可以使用 `SELECT pg_terminate_backend(pid)` 语句释放数据库连接，使用语句释放与这三个 ip 相关的数据库连接: `select pg_terminate_backend(pid) from pg_stat_activity where client_addr in ('100.104.205.90','100.104.205.83') `,过了一会数据库连接恢复正常了。

## 小结

本文通过阿里云数据库连接过高的问题，分析遇到此类问题时如何排查并解决。

## 参考

- [https://help.aliyun.com/zh/dms/configure-an-ip-address-whitelist](https://help.aliyun.com/zh/dms/configure-an-ip-address-whitelist)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Falliyunrdserr%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/alliyunrdserr/#top "Go to Top (Alt + G)")

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

## Kubernetes Resource Management
前言 Kubernetes 的 pod 可以按照节点的资源进行调度，默认情况下 pod 能够使用节点的全部资源，这样往往会出现因为节点自身运行的一些驱动及 Kubernetes 系统守护进程，导致资源不足的问题。 例如有一个应用在运行中使用了大量的系统资源，导致 kubelet 和 apiserver 的心跳出现故障，导致节点处于 Not Ready 的状态，节点出现 Not Ready 的状况后，过一会儿会将 pod 调度到其它 node 节点上运行，往往会导致节点雪崩，一个接一个的出现 Not Ready 状况。
那么如何解决这个问题呢？这时可以通过 为 Kubernetes 集群配置资源预留，kubelet 暴露了一个名为 Node Allocatable 的特性，有助于为系统守护进程预留计算资源，Kubernetes 也是推荐集群管理员按照每个节点上的工作负载来配置 Node Allocatable。
Node Allocatable Kubernetes 节点上的 Allocatable 被定义为 Pod 可用计算资源量。调度器不会超额申请 Allocatable。目前支持 CPU、内存 和 存储 这几个参数。可以通过 kubectl describe node 命令查看节点可分配资源的数据： 可以看到有 Capacity 和 Allocatable 两个内容，Allocatable 这个就是节点可分配资源，由于没有设置，所以默认 Capacity 和 Allocatable 是一致的。
Capacity 是节点所有的系统资源，kube-reserved 是给 kube 组件预留的资源，system-reserved 是给系统进程预留的资源，eviction-hard 是 Kubelet 的驱逐阈值。
...

 [post link to Kubernetes 系统资源预留](https://jasminides.com/posts/kubernetes_resource_reservation/)

前言 我们知道 kubernetes 内部服务之间是通过 service 进行相互访问的，那么如果现在有一个非 kubernetes 部署的服务，我们可以也通过 service 进行内部交互使用吗？答案是可以，我们可以使用 service 的 ExternalName 类型将 service 映射到外部服务上。
最近需要将一个外部服务映射到 kubernetes service 上，通过查找资料学习，本文记录如何将 kubernetes service 映射到外部服务的流程步骤。
外部域名映射内部 service 先讲解如何将外部服务通过域名的方式映射到内部 service 上，通过配置 externalName 字段来配置映射关系。例如，以下 Service 定义将 test 命名空间中的 my-service 服务映射到 my.overstarry.vip:
apiVersion: v1 kind: Service metadata: name: my-service namespace: test spec: type: ExternalName externalName: my.overstarry.vip 虽然 externalName 也支持填写 ip 地址，但不会被 kubernetes 解析，如果需要使用 ip 地址，可以使用无头服务 Headless，下文会进行介绍。
外部服务 ip 映射 service 接下来介绍没有域名的外部服务和 service 如何进行映射。上文讲过虽然 externalName 也支持填写 ip 地址，但不会被 kubernetes 解析，如果需要，则应该使用 Headless Service 进行映射。
...

 [post link to Kubernetes ExternalName](https://jasminides.com/posts/kubernetes_externalname/)

前言 最近在使用 Kubernetes 查看 pod 日志时，发现 pod 日志显示的 ip 不是真实的请求者 ip, 而是 Node 节点的 ip。通过查阅资料发现可以通过设置 externalTrafficPolicy 来显示真实的 IP。
本文对 externaltrafficpolicy 进行一个简单的介绍。
简介 ExternalTrafficPolicy 是 Kubernetes Service 对象的一个属性，它决定了流量如何从集群外部访问 Service。有两个可选值：Cluster 和 Local。
Cluster 模式： 在 Cluster 模式下，流量将通过负载均衡器分发到 Service 的所有 Pod 上。这是传统的负载均衡方式，适用于需要水平扩展和容错的场景。负载均衡器会将流量平均分配给所有可用的 Pod，从而实现负载均衡。
Local 模式： 在 Local 模式下，流量将直接访问与请求最近的节点上运行的 Pod。这种方式避免了负载均衡器的介入，直接将流量定向到本地的 Pod 上。这样可以减少延迟，并且在负载均衡器发生故障时仍然保持可用性。
区别 两种模式有什么区别呢？
Cluster 模式 Cluster 模式是默认的模式，Kube-proxy 不管容器在哪个节点上，会公平的转发到某一个节点上，在转发时会替换掉源 ip，变成转发的上一个节点的 ip.原因是 Kube-proxy 在做转发的时候，会做一次 SNAT (source network address translation)，所以源 ip 变成了上一个节点的 ip 地址。
这个模式的优点是负载均衡比较好，缺点是由于转发，可能会有性能损耗。
Local 模式 Local 模式下，请求只转发给本机的容器，不会转发给其它节点的容器，保留了源 ip。
...

 [post link to Kubernetes externaltrafficpolicy 简介](https://jasminides.com/posts/kubernetes_externaltrafficpolicy/)

问题 最近在调用一个上传文件的接口时，发现接口调用响应状态码为 413，并且控制台显示跨域错误信息。查找了相关信息，得知 413 状态码表示请求的包体过大导致的。
出现这种情况，我想到了 2 种解决方案：1) 调整上传文件的方式 2) 调整网关的参数。
综合目前的现况，采取了第二种方式调整网关客户端请求体最大值的参数。
解决 通过查阅 nginx ingress 的文档，得知可以添加 nginx.ingress.kubernetes.io/proxy-body-size 注解来设置请求体的最大值，设置 nginx.ingress.kubernetes.io/proxy-body-size 值为合适的值后，再请求接口发现接口顺利响应。
小结 本文介绍了客户端请求接口时，由于 nginx 默认 proxy-body-size 参数太小，导致请求 413 的问题及相应的解决方案。
参考 https://opendocs.alipay.com/support/01rb44 https://nginx.org/en/docs/http/ngx\_http\_core\_module.html#client\_max\_body\_size https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md#custom-max-body-size

 [post link to Nginx Ingress http 请求 413 状态码问题及解决方法](https://jasminides.com/posts/nginx-ingress_http%E8%AF%B7%E6%B1%82413%E9%97%AE%E9%A2%98%E5%8F%8A%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95/)

本文我来讲解 Kubernetes 中的一个重要概念：容器的健康检查。
介绍 在 Kubernetes 中，你可以为 Pod 里的容器定义一个健康检查“探针”（Probe）。 这样，kubelet 就会根据这个 Probe 的返回值决定这个容器的状态，而不是直接以容器镜像是否运行（来自 Docker 返回的信息）作为依据。 这种机制，是生产环境中保证应用健康存活的重要手段。
k8s 主要有三种健康检查的探针：1) LivenessProbe 存活探针 2) ReadinessProbe 就绪探针 3) StartupProbe 启动探针
kubelet 使用存活探针来确定什么时候要重启容器。例如，存活探针可以探测到应用死锁（应用程序在运行，但是无法继续执行后面的步骤）情况。重启这种状态下的容器有助于提高应用的可用性，即使其中存在缺陷。
存活探针的常见模式是为就绪探针使用相同的低成本 HTTP 端点，但具有更高的 failureThreshold。这样可以确保在硬性终止 Pod 之前，将观察到 Pod 在一段时间内处于非就绪状态。
kubelet 使用就绪探针可以知道容器何时准备好接受请求流量，当一个 Pod 内的所有容器都就绪时，才能认为该 Pod 就绪。这种信号的一个用途就是控制哪个 Pod 作为 Service 的后端。若 Pod 尚未就绪，会被从 Service 的负载均衡器中剔除。
kubelet 使用启动探针来了解应用容器何时启动。如果配置了这类探针，你就可以控制容器在启动成功后再进行存活性和就绪态检查，确保这些存活、就绪探针不会影响应用的启动。启动探针可以用于对慢启动容器进行存活性检测，避免它们在启动运行之前就被杀掉。
probe 介绍 接下来我来讲解用的较多的 2 个探针：1) LivenessProbe 存活探针 2) ReadinessProbe 就绪探针
LivenessProbe 许多应用由于长时间运行导致程序异常，需要重启服务才能继续正常使用，Kubernetes 提供了存活探针 (LivenessProbe) 来发现并处理这种情况。
我们先创建一个 pod, pod 的文件如下：
...

 [post link to Kubernetes Health check](https://jasminides.com/posts/kubernetes-healthcheck/)

前言 最近看了 k8s 的书，学习了一些新的知识，将会分几篇来介绍学习到的知识，本文来先介绍 k8s 中如何修改 pod 的 hosts 文件。
我们知道当 DNS 出现问题时，可以向 Pod 的/etc/hosts 文件添加条目来提供主机名解析 Pod 级别覆盖。该如何向 hosts 文件中添加条目呢？可以使用 PodSpec 中的 HostAliases 字段添加自定义条目。
虽然我们也可以直接进入 pod 修改 host 文件来实现，但这样 pod 重建时会被覆盖，所以我们应该使用 HostAliases 来进行修改，因为该文件会由 Kubelet 管理，并且 可以在 Pod 创建/重启过程中被重写。
使用 我们该如何操作呢，接下来由我来介绍使用步骤：
1 先创建 Deployment YAML 文件来创建后台运行的 busybox pod
apiVersion: apps/v1 kind: Deployment metadata: name: busybox-deployment spec: replicas: 1 selector: matchLabels: app: busybox template: metadata: labels: app: busybox spec: containers: - name: busybox image: busybox args: \[ "sleep", "3600" \] resources: limits: memory: "128Mi" cpu: "500m" requests: memory: "64Mi" cpu: "250m" volumeMounts: - name: busybox-volume mountPath: /data volumes: - name: busybox-volume emptyDir: {} 查看 pod ip
...

 [post link to Kubernetes pod 修改 hosts 文件](https://jasminides.com/posts/kubernetes_pod%E4%BF%AE%E6%94%B9hosts%E6%96%87%E4%BB%B6/)

今天我来简单介绍 kubernetes 生态中一个重要一环 - 包管理工具 Helm。
介绍 Helm 是 Kubernetes 的开源包管理器。它提供了提供、共享和使用为 Kubernetes 构建的软件的能力。
Helm 于 2015 年在 Deis 创建，后来被微软收购。现在称为 Helm Classic 的是在当年 11 月的首届 KubeCon 上推出的。2016 年 1 月，Helm Classic 与谷歌的 Kubernetes 部署管理器合并到现在是 Helm 主要项目的存储库中。
该项目目前拥有超过 30,000 个 GitHub stars，每月从全球获得超过 200 万次下载。2020 年 4 月，Helm 在 CNCF 中获得毕业。
安装 Helm 二进制安装 1 打开 https://github.com/helm/helm/releases , 下载你需要的版本 2 解压安装包 3 将文件夹中的 helm 二进制文件移动到相应的位置
脚本安装 helm 官方提供了一个安装的脚本：
$ curl -fsSL -o get\_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 $ chmod 700 get\_helm.sh $ ./get\_helm.sh 除了以上 2 种安装方式，你还可以通过各个操作系统的包管理工具安装和编译源码安装，这里就不过多赘述了。
...

 [post link to Helm 介绍及使用](https://jasminides.com/posts/helm%E4%BB%8B%E7%BB%8D%E5%8F%8A%E4%BD%BF%E7%94%A8/)

起因 最近在使用 k8s 部署应用时，我使用 ConfigMaps 的方式来挂载应用的配置文件。在我的知识储备中，k8s 修改 cm 的内容，pod 里的配置文件应该也会同步更新才是，但是我进入 pod , 发现配置还是旧版本没有更新，需要重启 pod 才会生效。
问题 那为什么配置没有及时更新呢？通过查阅资料，我发现使用 subPath 挂载的容器不会接收到配置更新。这是为什么呢，相比于没有使用 subPath 有什么区别呢？
subPath 使用了符号链接的方式挂载文件，容器内的文件是一个链接到存储在一个隐藏的带有时间戳目录中的同名文件。当 configMaps 更新时，符号链接会更新，但挂载在容器中的文件绑定保持不变。
解决 使用 path 字段为特定 ConfigMap 项指定所需的文件路径 具体如下：
apiVersion: v1 kind: Pod metadata: name: dapi-test-pod spec: containers: - name: test-container image: registry.k8s.io/busybox command: \[ "/bin/sh","-c","cat /etc/config/keys" \] volumeMounts: - name: config-volume mountPath: /etc/config volumes: - name: config-volume configMap: name: special-config items: - key: SPECIAL\_LEVEL path: keys restartPolicy: Never 亲测这样是可以正常更新的，但同目录下的其它文件会删除掉，看了几个相关的 issues , 发现你还可以手动创建符号链接到相应的文件夹，
小结 使用 subPath 挂载配置至容器时，配置更新时，容器内的配置不能同步更新，这是 k8s 官方处于各种原因做出的限制，目前还没有很好的办法来解决这个问题。
参考 https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#mounted-configmaps-are-updated-automatically https://github.com/kubernetes/kubernetes/issues/50345 https://github.com/kubernetes/kubernetes/blob/master/pkg/volume/util/atomic\_writer.go

 [post link to Kubernetes Configmaps mounted with subPath not update when changed](https://jasminides.com/posts/kubernetes-configmaps-subpath-no-reload/)

安装 Metrics Server 有了 Metrics Server，用户就可以访问 Kubernetes 核心监控数据（core metrics）。这其中包括了 Pod、Node、容器、Service 等主要 Kubernetes 核心概念的 Metrics。
Resource MetricsAPI: https://github.com/kubernetes/community/blob/master/contributors/design-proposals/instrumentation/resource-metrics-api.md kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml 部署 Prometheus kube-prometheus 下载存储库 git clone https://github.com/prometheus-operator/kube-prometheus 使用 manifests 中的配置文件创建监控 stack cd kube-prometheus kubectl create -f manifests/setup until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done kubectl create -f manifests/ 访问 dashboards 通过 kubectl --namespace monitoring port-forward svc/prometheus-k8s 9090 就能展现prometheus ui grafana
kubectl --namespace monitoring port-forward svc/grafana 3000 默认账户密码 admin/admin，进入后会要求修改密码，可以看到已经有了预添加了数据源 可以看到有了许多 K8S 监控的默认看板 ...

 [post link to Prometheus_operato](https://jasminides.com/posts/prometheus_operato/)

起因 在我们日常使用 k8s 中，可能会遇到这样的情况：在删除 namespace 时，往往会遇到资源没有被删除的情况，资源处于 terminating 的状态，这时我们该如何解决了，寻找到的解决方法往往是如下：
1 运行以下命令查看处于 terminating 状态的资源 (这里以 namespace 为例):
kubectl get namespaces
2 选择一个 Terminating namespace，并查看 namespace 中的 finalizer。运行以下命令：
kubectl get namespace <terminating-namespace> -o yaml
得到类似这样的信息：
apiVersion: v1 kind: Namespace metadata: creationTimestamp: "2021-01-20T15:18:06Z" deletionTimestamp: "2021-01-21T02:50:02Z" name: <terminating-namespace> resourceVersion: "3249493" selfLink: /api/v1/namespaces/knative-eventing uid: f300ea38-c8c2-4653-b432-b66103e412db spec: finalizers: - kubernetes status: phase: Terminating 3 导出 json 格式到 tmp.json:
...

 [post link to K8s_Finalizers](https://jasminides.com/posts/k8s_finalizers/) [Go to Top (Alt + G)](https://jasminides.com/tags/kubernetes/#top "Go to Top (Alt + G)")

## Kubernetes Resource Reservation
目录

- [前言](https://jasminides.com/posts/kubernetes_resource_reservation/#%e5%89%8d%e8%a8%80)
- [Node Allocatable](https://jasminides.com/posts/kubernetes_resource_reservation/#node-allocatable)
  - [设置 Kube-reserved](https://jasminides.com/posts/kubernetes_resource_reservation/#%e8%ae%be%e7%bd%ae-kube-reserved)
  - [system-reserved 设置](https://jasminides.com/posts/kubernetes_resource_reservation/#system-reserved-%e8%ae%be%e7%bd%ae)
  - [设置 eviction-hard](https://jasminides.com/posts/kubernetes_resource_reservation/#%e8%ae%be%e7%bd%ae-eviction-hard)
- [小结](https://jasminides.com/posts/kubernetes_resource_reservation/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/kubernetes_resource_reservation/#%e5%8f%82%e8%80%83)

## 前言

Kubernetes 的 pod 可以按照节点的资源进行调度，默认情况下 pod 能够使用节点的全部资源，这样往往会出现因为节点自身运行的一些驱动及 Kubernetes 系统守护进程，导致资源不足的问题。
例如有一个应用在运行中使用了大量的系统资源，导致 kubelet 和 apiserver 的心跳出现故障，导致节点处于 Not Ready 的状态，节点出现 Not Ready 的状况后，过一会儿会将 pod 调度到其它 node 节点上运行，往往会导致节点雪崩，一个接一个的出现 Not Ready 状况。

那么如何解决这个问题呢？这时可以通过 为 Kubernetes 集群配置资源预留，kubelet 暴露了一个名为 Node Allocatable 的特性，有助于为系统守护进程预留计算资源，Kubernetes 也是推荐集群管理员按照每个节点上的工作负载来配置 Node Allocatable。

## Node Allocatable

Kubernetes 节点上的 Allocatable 被定义为 Pod 可用计算资源量。调度器不会超额申请 Allocatable。目前支持 CPU、内存 和 存储 这几个参数。可以通过 `kubectl describe node` 命令查看节点可分配资源的数据：
![img.png](https://jasminides.com/img/kubernetes_revserve_compute_resources/img.png)

可以看到有 Capacity 和 Allocatable 两个内容，Allocatable 这个就是节点可分配资源，由于没有设置，所以默认 Capacity 和 Allocatable 是一致的。

Capacity 是节点所有的系统资源，kube-reserved 是给 kube 组件预留的资源，system-reserved 是给系统进程预留的资源，eviction-hard 是 Kubelet 的驱逐阈值。

因此节点的可用资源大概为 `Node Capacity - Kube-reserved - system-reserved - eviction-hard`,当节点的使用资源超过可用大小时，会将 pod 驱逐到其它节点。

### 设置 Kube-reserved

先来设置 Kube-reserved ,要配置 Kube-reserved，需要把 kubelet 的 –kube-reserved-cgroup 标志的值设置为 kube 守护进程的父控制组。不过需要注意，如果 –kube-reserved-cgroup 不存在，Kubelet 不会创建它，启动 Kubelet 将会失败。，修改 node 节点的 kubelet 配置文件，添加以下配置：

```yaml
enforceNodeAllocatable:
- pods
- kube-reserved
kubeReserved:
  cpu: 500m
  memory: 1Gi
  ephemeral-storage: 1Gi
kubeReservedCgroup: /kubelet.slice

```

复制

修改完重启服务，发现服务启动失败，查看日志，发现 cgroup 没创建，创建相应的路径即可：

```log
Mar 09 14:22:47 node01 kubelet[4800]: E0309 14:22:47.058618    4800 kubelet.go:1542] "Failed to start ContainerManager" err="Failed to enforce Kube Reserved Cgroup Limits on \"/kubelet.slice\": cgroup [\"kubelet\"] has some missing paths: /sys/fs/cgroup/memory/kubelet.slice, /sys/fs/cgroup/pids/kubelet.slice, /sys/fs/cgroup/hugetlb/kubelet.slice, /sys/fs/cgroup/cpuset/kubelet.slice, /sys/fs/cgroup/cpu,cpuacct/kubelet.slice, /sys/fs/cgroup/systemd/kubelet.slice, /sys/fs/cgroup/cpu,cpuacct/kubelet.slice"
复制
```

```shell
mkdir -p /sys/fs/cgroup/cpu,cpuacct/kubelet.slice
mkdir -p /sys/fs/cgroup/memory/kubelet.slice
mkdir -p /sys/fs/cgroup/systemd/kubelet.slice
mkdir -p /sys/fs/cgroup/pids/kubelet.slice
mkdir -p /sys/fs/cgroup/cpu,cpuacct/kubelet.slice
mkdir -p /sys/fs/cgroup/cpuset/kubelet.slice
mkdir -p /sys/fs/cgroup/hugetlb/kubelet.slice

```

复制

创建完重启 kubelet 服务，发现服务恢复正常了，再次查看节点信息，发现 Allocatable 值已经修改成功。

![img_1.png](https://jasminides.com/img/kubernetes_revserve_compute_resources/img_1.png)

### system-reserved 设置

system-reserved 也可以使用同样的方式进行设置，同样需要注意的是同样需要配置 system-reserved-cgroup 参数，这里就不过多赘述了。

### 设置 eviction-hard

如何修改驱逐阈值了，同样修改 kubelet 的配置文件，添加以下配置：

```yaml
evictionHard:
  memory.available:  "100Mi"
  nodefs.available:  "10%"
  nodefs.inodesFree: "5%"
  imagefs.available: "15%"

```

复制

当节点的内存达到保留值以下时，会进行 pod 的驱逐。配置完，再次查看节点的可使用资源，可以看到可分配资源再次减少。

## 小结

本文讲解了如何为 Kubernetes 节点设置可分配的资源限制，通过设置节点可分配资源大小，可以提高 Kubernetes 系统的稳定性，但需要注意的是配置参数时，需要注意参数的大小，不当的参数可能会导致系统出现异常。

## 参考

- [https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/](https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/)
- [https://cloud.tencent.com/developer/article/1774753](https://cloud.tencent.com/developer/article/1774753)
- [https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/](https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fkubernetes_resource_reservation%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/kubernetes_resource_reservation/#top "Go to Top (Alt + G)")

## Atop Tool Overview
前言 最近出现了服务器 cpu、内存升高导致服务器宕机的问题，发生宕机后，往往由于对系统资源数据收集的不齐全，导致无法快速查明发生宕机的原因。在通过云厂商客服和网络相关资料帮助下，了解了 atop 这个工具，本机对 atop 的安装及使用进行介绍。
atop 介绍 atop 是一款用于监控 Linux 系统资源与进程的工具，能够报告所有进程的活动。其以一定的频率记录系统和进程活动，采集的数据包含 CPU、内存、磁盘、网络的资源使用情况和进程运行情况，并能以日志文件的方式保存在磁盘中。对于每个进程，会显示 CPU 使用率、内存增长、磁盘使用率、优先级、用户名、状态和退出码等。当服务器出现问题后，可以根据相应的 atop 日志文件进行分析。
安装 atop 不是系统的内部自带命令，需要进行安装，接下来以 Ubuntu 系统为例子，介绍如何安装 atop 命令。
1 更新软件源
执行 sudo apt update 进行软件源的更新。
2 安装 atop
执行 sudo apt install atop 命令安装 atop。
配置 安装完 atop 后，可以使用 atop 的默认配置使用，也可根据使用情况修改默认配置，atop 默认配置在 /etc/sysconfig/atop,查看默认配置文件内容：
\# /etc/default/atop # see man atoprc for more possibilities to configure atop execution LOGOPTS="-R" LOGINTERVAL=600 LOGGENERATIONS=28 LOGPATH=/var/log/atop LOGINTERVAL 是监控周期，默认 600s，LOGGENERATIONS 是日志文件保留周期，默认是 28 天，可以根据具体的需求进行修改。
...

 [post link to atop 工具介绍及使用](https://jasminides.com/posts/atop/) [Go to Top (Alt + G)](https://jasminides.com/tags/atop/#top "Go to Top (Alt + G)")

## Atop Tool Overview
目录

- [前言](https://jasminides.com/posts/atop/#%e5%89%8d%e8%a8%80)
- [atop 介绍](https://jasminides.com/posts/atop/#atop-%e4%bb%8b%e7%bb%8d)
- [安装](https://jasminides.com/posts/atop/#%e5%ae%89%e8%a3%85)
- [配置](https://jasminides.com/posts/atop/#%e9%85%8d%e7%bd%ae)
- [使用](https://jasminides.com/posts/atop/#%e4%bd%bf%e7%94%a8)
- [分析日志](https://jasminides.com/posts/atop/#%e5%88%86%e6%9e%90%e6%97%a5%e5%bf%97)
- [小结](https://jasminides.com/posts/atop/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/atop/#%e5%8f%82%e8%80%83)

## 前言

最近出现了服务器 cpu、内存升高导致服务器宕机的问题，发生宕机后，往往由于对系统资源数据收集的不齐全，导致无法快速查明发生宕机的原因。在通过云厂商客服和网络相关资料帮助下，了解了 atop 这个工具，本机对 atop 的安装及使用进行介绍。

## atop 介绍

atop 是一款用于监控 Linux 系统资源与进程的工具，能够报告所有进程的活动。其以一定的频率记录系统和进程活动，采集的数据包含 CPU、内存、磁盘、网络的资源使用情况和进程运行情况，并能以日志文件的方式保存在磁盘中。对于每个进程，会显示 CPU 使用率、内存增长、磁盘使用率、优先级、用户名、状态和退出码等。当服务器出现问题后，可以根据相应的 atop 日志文件进行分析。

## 安装

atop 不是系统的内部自带命令，需要进行安装，接下来以 Ubuntu 系统为例子，介绍如何安装 atop 命令。

1 更新软件源

执行 `sudo apt update` 进行软件源的更新。

2 安装 atop

执行 `sudo apt install atop` 命令安装 atop。

![img.png](https://jasminides.com/img/atop/img.png)

## 配置

安装完 atop 后，可以使用 atop 的默认配置使用，也可根据使用情况修改默认配置，atop 默认配置在 `/etc/sysconfig/atop`,查看默认配置文件内容：

```text
# /etc/default/atop
# see man atoprc for more possibilities to configure atop execution

LOGOPTS="-R"
LOGINTERVAL=600
LOGGENERATIONS=28
LOGPATH=/var/log/atop

```

复制

LOGINTERVAL 是监控周期，默认 600s，LOGGENERATIONS 是日志文件保留周期，默认是 28 天，可以根据具体的需求进行修改。

## 使用

命令行输入 `atop` 命令即可使用，可以看到分为 2 块，上部是系统资源的使用情况，下部是没个进程的使用情况。
![img_1.png](https://jasminides.com/img/atop/img_1.png)

如果想看内存的使用情况，可以添加 `-m` 参数或者在 atop 命令输入 m

![img_2.png](https://jasminides.com/img/atop/img_2.png)

如果想看磁盘的情况可以输入 d，输入 c 可以查看各个进程的 cpu 使用情况。

atop 还有其它命令参数，具体可以执行 `atop -h` 查看。

## 分析日志

系统出现问题时，往往无法实时的查看系统资源的情况，这时我们可以通过 atop 的日志文件进行针对分析，atop 的日志文件存放在 `/var/log/atop` 路径下，
可以使用 `atop -r /var/log/atop/atop_xx ` 命令进行查看分析，执行命令后同样进入相应的界面，但此界面不会实时更新数据，我们可以使用相应的命令进行 cpu 内存 磁盘等资源的分析。

![img_3.png](https://jasminides.com/img/atop/img_3.png)

## 小结

本文介绍了 linux 上一个常用的系统资源进程监控工具，通过此工具可以分析系统资源和进程的使用情况，并且可以针对不同时间点进行分析研究。
atop 是一个复杂的工具，需要我们持续学习使用。

## 参考

- [https://www.lyyyuna.com/2018/07/04/perftest-atop/](https://www.lyyyuna.com/2018/07/04/perftest-atop/)

giscus

#### 0 个表情

#### 0 条评论

输入预览

[支持使用 Markdown 语法](https://guides.github.com/features/mastering-markdown/ "支持使用 Markdown 语法")

[使用 GitHub 登录](https://giscus.app/api/oauth/authorize?redirect_uri=https%3A%2F%2Fjasminides.com%2Fposts%2Fatop%2F)

[Go to Top (Alt + G)](https://jasminides.com/posts/atop/#top "Go to Top (Alt + G)")

## Linux System Monitoring
前言 最近出现了服务器 cpu、内存升高导致服务器宕机的问题，发生宕机后，往往由于对系统资源数据收集的不齐全，导致无法快速查明发生宕机的原因。在通过云厂商客服和网络相关资料帮助下，了解了 atop 这个工具，本机对 atop 的安装及使用进行介绍。
atop 介绍 atop 是一款用于监控 Linux 系统资源与进程的工具，能够报告所有进程的活动。其以一定的频率记录系统和进程活动，采集的数据包含 CPU、内存、磁盘、网络的资源使用情况和进程运行情况，并能以日志文件的方式保存在磁盘中。对于每个进程，会显示 CPU 使用率、内存增长、磁盘使用率、优先级、用户名、状态和退出码等。当服务器出现问题后，可以根据相应的 atop 日志文件进行分析。
安装 atop 不是系统的内部自带命令，需要进行安装，接下来以 Ubuntu 系统为例子，介绍如何安装 atop 命令。
1 更新软件源
执行 sudo apt update 进行软件源的更新。
2 安装 atop
执行 sudo apt install atop 命令安装 atop。
配置 安装完 atop 后，可以使用 atop 的默认配置使用，也可根据使用情况修改默认配置，atop 默认配置在 /etc/sysconfig/atop,查看默认配置文件内容：
\# /etc/default/atop # see man atoprc for more possibilities to configure atop execution LOGOPTS="-R" LOGINTERVAL=600 LOGGENERATIONS=28 LOGPATH=/var/log/atop LOGINTERVAL 是监控周期，默认 600s，LOGGENERATIONS 是日志文件保留周期，默认是 28 天，可以根据具体的需求进行修改。
...

 [post link to atop 工具介绍及使用](https://jasminides.com/posts/atop/)

Issue Recently, a Linux server has been experiencing high CPU usage, causing the server to become unresponsive and other processes to fail to execute smoothly. By using the top command to check resource usage, it can be seen that the kswapd0 process is consuming a large amount of CPU resources.
Cause and solution Based on my research, the kswapd0 process is responsible for managing virtual memory.
Typically, a Linux system comprises RAM, swap, and EXT4 components. The EXT4 partition is used to store regular files and can be created on either an HDD or an SSD, though it is relatively slower compared to RAM. RAM, commonly referred to as memory, is used for high-speed program execution. The swap partition, on the other hand, is used as additional virtual memory and is normally allocated on physical disks, especially on machines with limited physical RAM.
...

 [post link to Kswapd0 is consuming a lot of CPU.](https://jasminides.com/posts/kswapd0_consumes_a_lot_of_cpu/)

问题 最近一台 Linux 服务器经常出现 cpu 过高，导致服务器卡顿，其他进程不能顺利进行。通过 top 命令查看资源的占用情况，可以看到 Kswapd0 进程 消耗了大量的 cpu 资源。
原因及解决 通过搜索得知，Kswapd0 进程是用来管理虚拟内存的。
一般的 Linux 都会有 RAM，swap, 和 EXT4 这几个部分，EXT4 分区就是用来存放一般的文件，可以在机械硬盘或者 SSD 上划分出 ext4 分区来保存文件，相对 RAM（内存）来说要稍微慢一些，RAM 就是日常所说的内存，用来做程序运行时的高速缓存，而 SWAP 是交换分区，一般在物理内存比较小的机器上会划分一块物理磁盘来作为 swap 分区。
swap 分区是一款虚拟的 RAM，一般在 HDD/SSD 上，当物理内存比较小的时侯，可能经常缺内存，那么系统就会使用 swap 分区，将物理内存中的内容搬迁到 swap 分区中暂存。当可用物理内存比较小的时候，kswapd0 进程就会将相对比较不常用的程序移动到 swap 分区中，这个时候就可能造成这些程序比较卡顿。例如一台机器的内存是 4G，而要运行一个需要 5G 内存的程序，那么至少有 1G 的内存会放到 swap 分区中。kswapd0 移动内存的过程就会造成 CPU 的大量使用。要解决这个问题有这样几个方式。
1 修改 /etc/sysctl.conf 文件
echo vm.swappiness=0 \| sudo tee -a /etc/sysctl.conf
...

 [post link to Kswapd0 消耗大量 cpu](https://jasminides.com/posts/kswapd0%E6%B6%88%E8%80%97%E5%A4%A7%E9%87%8Fcpu/)

起因 在一次使用虚拟机的时候，发现 Linux 系统进入了 Initramfs，无法正常进入系统，推测可能是系统异常关机导致磁盘文件损坏导致的。
解决 网上搜寻了一些解决方法，普遍的推荐方法是使用 Linux 命令 fsck 命令来修复磁盘文件。
费了好大劲进入另一个系统使用 fsck.ext4 -f /dev/sda1 来检查修复磁盘文件 (我所使用的 linux 系统磁盘是 ext4 格式的)。
接下来我来介绍下 fsck 的使用。
fsck fsck（file system consistency check）是 Unix 和类 Unix 系统上用于检查文件系统完整性的工具。
语法：fsck \[选项\] \[文件系统\]
常见参数：
-f 强制检查文件系统，不管是否有损坏 -p 自动修复文件系统错误 -q 做一个快速检查，以确定文件系统是否被干净地卸载。 -y 关闭互动模式，询问全部选择 y 参考 https://web.archive.org/web/20150529001726/http://www.manpagez.com/man/8/fsck/ https://zh.wikipedia.org/zh-hans/Fsck https://zh.wikipedia.org/wiki/Unix%E5%AE%9E%E7%94%A8%E7%A8%8B%E5%BA%8F%E5%88%97%E8%A1%A8

 [post link to Fsck](https://jasminides.com/posts/fsck/) [Go to Top (Alt + G)](https://jasminides.com/tags/linux/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Flinux%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801929305&bpp=3&bdt=185&idt=138&shv=r20250319&mjsv=m202503190101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=5199446100734&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95355339%2C31091181%2C95332923%2C31091146%2C95355301&oid=2&pvsid=1827170513218945&tmod=1981563694&uas=0&nvt=1&fsapi=1&fc=1920&brdim=130%2C130%2C130%2C130%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=157)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Mapping External Services
前言 我们知道 kubernetes 内部服务之间是通过 service 进行相互访问的，那么如果现在有一个非 kubernetes 部署的服务，我们可以也通过 service 进行内部交互使用吗？答案是可以，我们可以使用 service 的 ExternalName 类型将 service 映射到外部服务上。
最近需要将一个外部服务映射到 kubernetes service 上，通过查找资料学习，本文记录如何将 kubernetes service 映射到外部服务的流程步骤。
外部域名映射内部 service 先讲解如何将外部服务通过域名的方式映射到内部 service 上，通过配置 externalName 字段来配置映射关系。例如，以下 Service 定义将 test 命名空间中的 my-service 服务映射到 my.overstarry.vip:
apiVersion: v1 kind: Service metadata: name: my-service namespace: test spec: type: ExternalName externalName: my.overstarry.vip 虽然 externalName 也支持填写 ip 地址，但不会被 kubernetes 解析，如果需要使用 ip 地址，可以使用无头服务 Headless，下文会进行介绍。
外部服务 ip 映射 service 接下来介绍没有域名的外部服务和 service 如何进行映射。上文讲过虽然 externalName 也支持填写 ip 地址，但不会被 kubernetes 解析，如果需要，则应该使用 Headless Service 进行映射。
...

 [post link to Kubernetes ExternalName](https://jasminides.com/posts/kubernetes_externalname/) [Go to Top (Alt + G)](https://jasminides.com/tags/external/#top "Go to Top (Alt + G)")

## Kubernetes External Service Mapping
目录

- [前言](https://jasminides.com/posts/kubernetes_externalname/#%e5%89%8d%e8%a8%80)
- [外部域名映射内部 service](https://jasminides.com/posts/kubernetes_externalname/#%e5%a4%96%e9%83%a8%e5%9f%9f%e5%90%8d%e6%98%a0%e5%b0%84%e5%86%85%e9%83%a8-service)
- [外部服务 ip 映射 service](https://jasminides.com/posts/kubernetes_externalname/#%e5%a4%96%e9%83%a8%e6%9c%8d%e5%8a%a1-ip-%e6%98%a0%e5%b0%84-service)
- [小结](https://jasminides.com/posts/kubernetes_externalname/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/kubernetes_externalname/#%e5%8f%82%e8%80%83)

## 前言

我们知道 kubernetes 内部服务之间是通过 service 进行相互访问的，那么如果现在有一个非 kubernetes 部署的服务，我们可以也通过 service 进行内部交互使用吗？答案是可以，我们可以使用 service 的 ExternalName
类型将 service 映射到外部服务上。

最近需要将一个外部服务映射到 kubernetes service 上，通过查找资料学习，本文记录如何将 kubernetes service 映射到外部服务的流程步骤。

## 外部域名映射内部 service

先讲解如何将外部服务通过域名的方式映射到内部 service 上，通过配置 externalName 字段来配置映射关系。例如，以下 Service 定义将 test 命名空间中的 my-service 服务映射到 my.overstarry.vip:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: test
spec:
  type: ExternalName
  externalName: my.overstarry.vip

```

复制

虽然 externalName 也支持填写 ip 地址，但不会被 kubernetes 解析，如果需要使用 ip 地址，可以使用无头服务 Headless，下文会进行介绍。

## 外部服务 ip 映射 service

接下来介绍没有域名的外部服务和 service 如何进行映射。上文讲过虽然 externalName 也支持填写 ip 地址，但不会被 kubernetes 解析，如果需要，则应该使用 Headless Service 进行映射。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: test
spec:
  clusterIP: None
  type: ClusterIP

---

apiVersion: v1
kind: Endpoints
metadata:
 name: test
subsets:
 - addresses:
     - ip: 10.0.1.10

```

复制

创建 service 不指定 selector，手动维护创建 endpoint，创建之后就可以通过 test 访问 10.0.1.10 这个外部服务。

## 小结

本文简单的介绍了 kubernetes 如何将 service 和 外部服务进行映射，通过查阅资料可以得知两种方式映射外部服务是没有经过中间层代理的，都是通过 DNS 劫持实现。通过外部服务映射的功能，我们可以使用不同命名空间的 service 访问不同的数据库。

## 参考

- [https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#externalname](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#externalname)

giscus

正在加载评论……

[Go to Top (Alt + G)](https://jasminides.com/posts/kubernetes_externalname/#top "Go to Top (Alt + G)")

## Kubernetes Service Mapping
前言 我们知道 kubernetes 内部服务之间是通过 service 进行相互访问的，那么如果现在有一个非 kubernetes 部署的服务，我们可以也通过 service 进行内部交互使用吗？答案是可以，我们可以使用 service 的 ExternalName 类型将 service 映射到外部服务上。
最近需要将一个外部服务映射到 kubernetes service 上，通过查找资料学习，本文记录如何将 kubernetes service 映射到外部服务的流程步骤。
外部域名映射内部 service 先讲解如何将外部服务通过域名的方式映射到内部 service 上，通过配置 externalName 字段来配置映射关系。例如，以下 Service 定义将 test 命名空间中的 my-service 服务映射到 my.overstarry.vip:
apiVersion: v1 kind: Service metadata: name: my-service namespace: test spec: type: ExternalName externalName: my.overstarry.vip 虽然 externalName 也支持填写 ip 地址，但不会被 kubernetes 解析，如果需要使用 ip 地址，可以使用无头服务 Headless，下文会进行介绍。
外部服务 ip 映射 service 接下来介绍没有域名的外部服务和 service 如何进行映射。上文讲过虽然 externalName 也支持填写 ip 地址，但不会被 kubernetes 解析，如果需要，则应该使用 Headless Service 进行映射。
...

 [post link to Kubernetes ExternalName](https://jasminides.com/posts/kubernetes_externalname/)

前言 最近在使用 Kubernetes 查看 pod 日志时，发现 pod 日志显示的 ip 不是真实的请求者 ip, 而是 Node 节点的 ip。通过查阅资料发现可以通过设置 externalTrafficPolicy 来显示真实的 IP。
本文对 externaltrafficpolicy 进行一个简单的介绍。
简介 ExternalTrafficPolicy 是 Kubernetes Service 对象的一个属性，它决定了流量如何从集群外部访问 Service。有两个可选值：Cluster 和 Local。
Cluster 模式： 在 Cluster 模式下，流量将通过负载均衡器分发到 Service 的所有 Pod 上。这是传统的负载均衡方式，适用于需要水平扩展和容错的场景。负载均衡器会将流量平均分配给所有可用的 Pod，从而实现负载均衡。
Local 模式： 在 Local 模式下，流量将直接访问与请求最近的节点上运行的 Pod。这种方式避免了负载均衡器的介入，直接将流量定向到本地的 Pod 上。这样可以减少延迟，并且在负载均衡器发生故障时仍然保持可用性。
区别 两种模式有什么区别呢？
Cluster 模式 Cluster 模式是默认的模式，Kube-proxy 不管容器在哪个节点上，会公平的转发到某一个节点上，在转发时会替换掉源 ip，变成转发的上一个节点的 ip.原因是 Kube-proxy 在做转发的时候，会做一次 SNAT (source network address translation)，所以源 ip 变成了上一个节点的 ip 地址。
这个模式的优点是负载均衡比较好，缺点是由于转发，可能会有性能损耗。
Local 模式 Local 模式下，请求只转发给本机的容器，不会转发给其它节点的容器，保留了源 ip。
...

 [post link to Kubernetes externaltrafficpolicy 简介](https://jasminides.com/posts/kubernetes_externaltrafficpolicy/) [Go to Top (Alt + G)](https://jasminides.com/tags/service/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fservice%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801954097&bpp=7&bdt=272&idt=229&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=5202652011236&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95353387&oid=2&pvsid=3947955660020493&tmod=78337315&uas=0&nvt=1&fsapi=1&fc=1920&brdim=40%2C40%2C40%2C40%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=247)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## CDN Cache Refresh Guide
前言 cdn 刷新是 cdn 使用过程中的一项重要的功能，通过刷新功能，您可以删除 CDN 节点上已经缓存的资源，并强制 CDN 节点回源站获取最新资源，适用于源站资源更新和发布、违规资源清理、域名配置变更等。
接下来将分别讲述 阿里云 CDN、AWS cloudfront、Cloudflare cdn 使用 go 语言进行 cdn 的刷新操作的。
阿里云刷新 cdn 如何刷新 阿里云 cdn 的缓存呢？只需使用 阿里云 openapi 的 go sdk 即可，通过查阅文档，我们只需使用 RefreshObjectCaches API 即可刷新阿里云 cdn 的缓存，RefreshObjectCaches 有以下参数：
ObjectPath: 刷新的url ,多个 url 使用换行符进行分隔 ObjectType: 刷新任务的类型，有以下类型 File（默认值）：文件刷新。 Directory：目录刷新。 Regex：正则刷新。 IgnoreParams：去参数刷新。去参数指的是去除请求 URL 中?及?之后的参数，去参数刷新指的是用户先通过接口提交去参数后的 URL，然后用户提交的待刷新 URL 将会与已缓存资源的 URL 进行去参数匹配，如果已缓存资源的 URL 去参数以后与待刷新 URL 匹配，那么 CDN 节点将对缓存资源执行刷新处理。 Force: 当回源内容和源站资源对比后不一致时，是否刷新对应目录下的资源。默认为 false。 下面是一个例子：
package main import ( cdn20180510 "github.com/alibabacloud-go/cdn-20180510/v4/client" openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client" util "github.com/alibabacloud-go/tea-utils/v2/service" "github.com/alibabacloud-go/tea/tea" "os" ) func CreateClient(accessKeyId \*string, accessKeySecret \*string) (result \*cdn20180510.Client, err error) { config := &openapi.Config{ AccessKeyId: accessKeyId, AccessKeySecret: accessKeySecret, } config.Endpoint = tea.String("cdn.ap-southeast-1.aliyuncs.com") result = &cdn20180510.Client{} result, err = cdn20180510.NewClient(config) return result, err } func main() { client, err := CreateClient(tea.String(os.Getenv("ALIBABA\_CLOUD\_ACCESS\_KEY\_ID")), tea.String(os.Getenv("ALIBABA\_CLOUD\_ACCESS\_KEY\_SECRET"))) if err != nil { return } refreshObjectCachesRequest := &cdn20180510.RefreshObjectCachesRequest{ ObjectPath: tea.String("http://example.com/image/1.png\\\\\n\\t\\thttp://aliyundoc.com/image/2.png"), } runtime := &util.RuntimeOptions{} \_, err = client.RefreshObjectCachesWithOptions(refreshObjectCachesRequest, runtime) if err != nil { return } return } aws cloudfront 接下来讲解 aws cloudfront 如何刷新 cdn，cloudfront 刷新缓存的操作叫使文件失效，通过查阅 cloudfront 的 API 文档，发现可以使用 CreateInvalidation 来创建失效。可以使用 aws go sdk 来进行操作。
...

 [post link to Go 刷新 cdn](https://jasminides.com/posts/go_refresh_cdn/)

最近在研究使用 google cloud 的 cdn 服务，本文就来讲解如何清除 cdn 的缓存。
本文介绍了几种清除 cdn 缓存的方法。
google cloud console 清除 第一种也是最简单的，就是直接从 google cloud console 后台进行操作，我们打开 console 后台，选择网络服务，点击负载均衡界面，选择我们要清除的 cdn 缓存所使用的负载均衡器，点击缓存页面， 输入想要 cdn 节点清除的路径即可。过了一会，就可以看到操作成功，相应的文件已经失效。 Google Cloud CLI 命令 第二种方法是使用 Google Cloud CLI 使 cdn 缓存文件失效。
Google Cloud CLI 安装 该怎么安装 Google Cloud CLI 呢，有 2 个办法：1) 直接下载安装二进制文件 2) 使用 Cloud Shell. 本文是使用 Cloud Shell 进行的操作。
使缓存内容失效 1 使用 gcloud compute url-maps list 列出目前所使用的负载均衡器
...

 [post link to Google Cloud 清除 CDN 缓存](https://jasminides.com/posts/googlecloud%E6%B8%85%E9%99%A4cdn%E7%BC%93%E5%AD%98/) [Go to Top (Alt + G)](https://jasminides.com/tags/cdn/#top "Go to Top (Alt + G)")

## CDN Cache Refresh Guide
目录

- [前言](https://jasminides.com/posts/go_refresh_cdn/#%e5%89%8d%e8%a8%80)
- [阿里云刷新 cdn](https://jasminides.com/posts/go_refresh_cdn/#%e9%98%bf%e9%87%8c%e4%ba%91%e5%88%b7%e6%96%b0-cdn)
- [aws cloudfront](https://jasminides.com/posts/go_refresh_cdn/#aws-cloudfront)
- [cloudflare](https://jasminides.com/posts/go_refresh_cdn/#cloudflare)
- [参考](https://jasminides.com/posts/go_refresh_cdn/#%e5%8f%82%e8%80%83)

## 前言

cdn 刷新是 cdn 使用过程中的一项重要的功能，通过刷新功能，您可以删除 CDN 节点上已经缓存的资源，并强制 CDN 节点回源站获取最新资源，适用于源站资源更新和发布、违规资源清理、域名配置变更等。

接下来将分别讲述 阿里云 CDN、AWS cloudfront、Cloudflare cdn 使用 go 语言进行 cdn 的刷新操作的。

## 阿里云刷新 cdn

如何刷新 阿里云 cdn 的缓存呢？只需使用 阿里云 openapi 的 go sdk 即可，通过查阅文档，我们只需使用 RefreshObjectCaches API 即可刷新阿里云 cdn 的缓存，RefreshObjectCaches 有以下参数：

```
ObjectPath: 刷新的url ,多个 url 使用换行符进行分隔
ObjectType: 刷新任务的类型，有以下类型
    File（默认值）：文件刷新。
    Directory：目录刷新。
    Regex：正则刷新。
    IgnoreParams：去参数刷新。去参数指的是去除请求 URL 中?及?之后的参数，去参数刷新指的是用户先通过接口提交去参数后的 URL，然后用户提交的待刷新 URL 将会与已缓存资源的 URL 进行去参数匹配，如果已缓存资源的 URL 去参数以后与待刷新 URL 匹配，那么 CDN 节点将对缓存资源执行刷新处理。
Force: 当回源内容和源站资源对比后不一致时，是否刷新对应目录下的资源。默认为 false。
复制
```

下面是一个例子：

```go
package main

import (
	cdn20180510 "github.com/alibabacloud-go/cdn-20180510/v4/client"
	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
	"os"
)

func CreateClient(accessKeyId *string, accessKeySecret *string) (result *cdn20180510.Client, err error) {
	config := &openapi.Config{
		AccessKeyId:     accessKeyId,
		AccessKeySecret: accessKeySecret,
	}
	config.Endpoint = tea.String("cdn.ap-southeast-1.aliyuncs.com")
	result = &cdn20180510.Client{}
	result, err = cdn20180510.NewClient(config)
	return result, err
}

func main() {
	client, err := CreateClient(tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")), tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")))
	if err != nil {
		return
	}

	refreshObjectCachesRequest := &cdn20180510.RefreshObjectCachesRequest{
		ObjectPath: tea.String("http://example.com/image/1.png\\\n\t\thttp://aliyundoc.com/image/2.png"),
	}
	runtime := &util.RuntimeOptions{}
	_, err = client.RefreshObjectCachesWithOptions(refreshObjectCachesRequest, runtime)
	if err != nil {
		return
	}

	return
}

```

复制

## aws cloudfront

接下来讲解 aws cloudfront 如何刷新 cdn，cloudfront 刷新缓存的操作叫使文件失效，通过查阅 cloudfront 的 API 文档，发现可以使用 CreateInvalidation 来创建失效。可以使用 aws go sdk 来进行操作。

这个 API 有以下参数：

```
InvalidationBatch: 必填
CallerReference： 用来表示请求唯一的值，防止发送重复的请求。
Paths： 失效的路径
复制
```

API 的 go 实现如下：

```go
func (c *Client) CreateInvalidation(ctx context.Context, params *CreateInvalidationInput, optFns ...func(*Options)) (*CreateInvalidationOutput, error) {
	if params == nil {
		params = &CreateInvalidationInput{}
	}

	result, metadata, err := c.invokeOperation(ctx, "CreateInvalidation", params, optFns, c.addOperationCreateInvalidationMiddlewares)
	if err != nil {
		return nil, err
	}

	out := result.(*CreateInvalidationOutput)
	out.ResultMetadata = metadata
	return out, nil
}

```

复制

接下来讲解 cloudflare 刷新 cdn 缓存。

## cloudflare

cloudflare 提供了以下方式来清除缓存：

- 单文件清除
- 清除全部
- 标记清除：由与提供的某个值相匹配的 Cache-Tag 响应标头提供服务的任何资产都将从缓存中清除。
- 按主机名清除：URL 中其主机与提供的某个值相匹配的任何资产都将从缓存中清除
- 按前缀清除：此目录中的所有资产都将从缓存中清除。

![img.png](https://jasminides.com/img/cdn_refresh_cache/img.png)

清除缓存的接口定义如下：

```
https://api.cloudflare.com/client/v4/zones/{identifier}/purge_cache
复制
```

有以下参数：

```
tags: 标记
hosts:
prefixes:
复制
```

下面是一个例子：

```go
package main

import (
	"fmt"
	"strings"
	"net/http"
	"io"
)

func main() {

	url := "https://api.cloudflare.com/client/v4/zones/identifier/purge_cache"

	payload := strings.NewReader("{\n  \"tags\": [\n    \"some-tag\",\n    \"another-tag\"\n  ]\n}")

	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("X-Auth-Email", "")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}

```

复制

除了使用 http 请求的方式，我们还可以使用 sdk 来进行缓存的删除。

## 参考

- [https://next.api.aliyun.com/api/Cdn/2018-05-10/RefreshObjectCaches](https://next.api.aliyun.com/api/Cdn/2018-05-10/RefreshObjectCaches)
- [https://developers.cloudflare.com/cache/how-to/purge-cache/](https://developers.cloudflare.com/cache/how-to/purge-cache/)
- [https://developers.cloudflare.com/api/operations/zone-purge](https://developers.cloudflare.com/api/operations/zone-purge)
- [https://github.com/aws/aws-sdk-go-v2/blob/service/cloudfront/v1.32.6/service/cloudfront/api\_op\_CreateInvalidation.go#L16](https://github.com/aws/aws-sdk-go-v2/blob/service/cloudfront/v1.32.6/service/cloudfront/api_op_CreateInvalidation.go#L16)
- [https://docs.aws.amazon.com/cloudfront/latest/APIReference/API\_CreateInvalidation.html](https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_CreateInvalidation.html)
- [https://github.com/cloudflare/cloudflare-go](https://github.com/cloudflare/cloudflare-go)

giscus

正在加载评论……

[Go to Top (Alt + G)](https://jasminides.com/posts/go_refresh_cdn/#top "Go to Top (Alt + G)")

## APISIX Gzip and gRPC
最近使用 Apisix 网关时，需要开启 gzip 功能，通过查阅资料学习，了解了几种开启 gzip 的方式，本文记录 2 种 Apisix 开启 gzip 的方式。
gzip 插件 我们可以使用 gzip 插件 针对某些路由开启 gzip，只需对路由使用 gzip 插件并配置一些插件属性即可。
接下来使用一个例子来演示 gzip 插件，使用 apisix admin api 创建一条路由，要注意的是本文的例子是使用 apisix 3.7 版本：
curl -i http://127.0.0.1:9180/apisix/admin/routes \ -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X POST -d ' { "uri": "/get", "plugins": { "gzip": { "buffers": { "number": 8 }, "comp\_level": 6, "disable": false, "types": "\*" } }, "upstream": { "nodes": \[ { "host": "httpbin.org", "port": 443, "weight": 1 } \], "timeout": { "connect": 6, "send": 6, "read": 6 }, "type": "roundrobin", "scheme": "https", "pass\_host": "pass", "keepalive\_pool": { "idle\_timeout": 60, "requests": 1000, "size": 320 } }, "status": 1 }' ...

 [post link to Apisix 开启 gzip](https://jasminides.com/posts/apisix_enabled_gzip/)

最近需要使用 apisix 来代理 gRPC 服务，本文记录一下 apisix 代理 gRPC 服务以及实践过程中遇到的一些问题。
准备 在接下来的步骤前，我们需要准备一个 gRPC 服务，我们使用 kratos 简单启动一个 gRPC 服务：
$ kratos new hellowrold $ cd helloworld $ kratos run 一个简单的 gRPC 服务就启动了，我们先直接请求 gRPC 服务看看，通过 postman 请求接口后，接口顺利返回相应的值。
接下来我们开始本篇的主要内容：apisix 代理服务。
apisix 代理 gRPC 服务 我们使用 apisix admin 接口创建 Route: upstream 的 scheme 指定为 grpc 或 grpcs,nodes 指定需要代理的服务地址。
curl http://127.0.0.1:9180/apisix/admin/routes/1 -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X PUT -d ' { "methods": \["POST", "GET"\], "uri": "/helloworld.v1.Greeter/SayHello", "upstream": { "scheme": "grpc", "type": "roundrobin", "nodes": { "127.0.0.1:9001": 1 } } }' ...

 [post link to apisix 代理 gRPC 服务](https://jasminides.com/posts/apisix_proxy_grpc_service/)

前言 最近需要忽略请求 uri 大小写，即不管 uri 的大小写都返回小写 uri 所请求的响应内容，例如请求 xx.vip/A 实际请求 xx.vip/a, 本文主要以 apisix 来讲解如何实现这个功能。
解决 遇到这个需求，首先肯定采用 apisix 的插件来实现，根据前面多次的经验，这个功能应该可以使用 serverless 插件中的 serverless-pre-function 插件来实现，具体的流程如下：
1 获取请求的 uri 2 将 uri 转为小写 3 修改请求的 uri
具体的插件内容如下：
"serverless-pre-function": { "\_meta": { "disable": false }, "functions": \[ "return function(conf, ctx) local uri = ctx.var.uri;ctx.var.uri= string.lower(uri);ngx.log(ngx.ERR, \\"match uri \\", ctx.var.uri ); end" \], "phase": "rewrite" } 添加插件后，再次请求路径，发现请求结果还是没有变，查看日志发现 uri 修改成功了，不知为何还是没有修改成功。
后面又仔细研究了 proxy-rewrite 插件中修改 uri 的代码，发现它是使用了 nginx 标准的函数 ngx.req.set\_uri 来赋值新的 uri。
...

 [post link to Apisix 忽略 uri 大小写](https://jasminides.com/posts/apisix%E5%BF%BD%E7%95%A5uri%E5%A4%A7%E5%B0%8F%E5%86%99/)

前言 前段时间在使用 apisix 添加路由时，需要将 http 转为 https, 在配置 http\_to\_https 后，访问相应网址时发现 https 的端口不是我们所配置的默认端口 443，而是 9443 端口。
可以看到访问 http://localhost 会跳转至错误的地址：https://localhost:9443/ ,正确的地址应该是 https://localhost，这是怎么回事呢？
分析 接下来我来简单对问题进行简单分析。
我是采用 docker 的方式部署的 apisix，这是我们的配置文件：
version: "3" services: apisix-dashboard: image: apache/apisix-dashboard:3.0.0-alpine restart: always volumes: - ./dashboard\_conf/conf.yaml:/usr/local/apisix-dashboard/conf/conf.yaml ports: - "9000:9000" networks: apisix: apisix: image: apache/apisix:${APISIX\_IMAGE\_TAG:-3.2.0-debian} restart: always volumes: - ./apisix\_conf/config.yaml:/usr/local/apisix/conf/config.yaml:ro depends\_on: - etcd ##network\_mode: host ports: - "9180:9180/tcp" - "80:9080/tcp" - "9091:9091/tcp" - "443:9443/tcp" - "9092:9092/tcp" networks: apisix: etcd: image: bitnami/etcd:3.4.15 restart: always volumes: - etcd\_data:/bitnami/etcd environment: ETCD\_ENABLE\_V2: "true" ALLOW\_NONE\_AUTHENTICATION: "yes" ETCD\_ADVERTISE\_CLIENT\_URLS: "http://etcd:2379" ETCD\_LISTEN\_CLIENT\_URLS: "http://0.0.0.0:2379" ports: - "2379:2379/tcp" networks: apisix: web1: image: nginx:1.19.0-alpine restart: always volumes: - ./upstream/web1.conf:/etc/nginx/nginx.conf ports: - "9081:80/tcp" environment: - NGINX\_PORT=80 networks: apisix: networks: apisix: driver: bridge volumes: etcd\_data: driver: local 可以看到我们将 apisix 容器的 http 端口和 https 端口映射为 80 和 443，按照常理来说，http\_to\_https 后的端口应该也是 443 端口才对。我猜测重定向时，apisix 还是采用配置文件中设定的 https 端口才导致跳转的 url 端口错误。
...

 [post link to Apisix Docker 部署网站重定向端口错误问题](https://jasminides.com/posts/apisix-docker%E9%83%A8%E7%BD%B2%E9%87%8D%E5%AE%9A%E5%90%91%E9%97%AE%E9%A2%98/)

今天我来讲讲如何备份 apisix 的数据，主要是路由、服务、上游等数据。本文中的 apisix 版本为 apisix 3.1.0 版本。
接下来由我来介绍几种备份方法。
dashboard 导出备份 介绍的第一种方法是使用 apisix dashboard 进行数据导出，但这种方法有许多缺陷，只能导出 route 数据，其他服务、ssl 数据都不能导出，而且新版本 (3.0+)dashboard 导出的路由不包含上游服务的数据，不方便进行快速的路由迁移复制 (我猜测可能是害怕上游服务信息不一致导致路由错误)。
接下来就来介绍如何进行导入导出。
1 我们打开 dashboard
2 选择要导出的路由，点击 export openapi
3 在新的 apisix dashboard 导入刚刚导出的 openapi 文件并填写相应的信息，导入成功后就可以看到导入的路由信息，相应路由的服务需要补充填写。
根据 admin api 编写相应的脚本 apisix 提供了各种 route、service 的 admin api 数据接口，我们可以根据官方提供的接口编写相应的脚本。
使用 etcd 备份方案 由于 apisix 默认采用 etcd 进行数据存储，我们可以备份 etcd 数据，到新的 apisix 集群导入备份的数据。
由于我对 etcd 的运维不太熟悉，想要了解 etcd 备份快照，可以查看这条链接。
...

 [post link to apisix 数据备份](https://jasminides.com/posts/apisix%E6%95%B0%E6%8D%AE%E5%A4%87%E4%BB%BD/)

最近在研究 apisix 插件，想要研究插件的执行流程，为了了解插件的具体运行流程，查看了几种方法来调试:1. inspect plugin 2. 自定义插件调试 等等。
本文介绍了添加启用自定义插件。
简单修改插件 最近在研究 apisix 的 proxy-cache 插件，本文就以 proxy-cache 插件为例子来讲解 docker 环境下如何自定义插件。
我们先从 apisix 官方 git 库拷贝 proxy-cache 插件代码到本地文件夹。我们对插件的内容进行修改删除，并将插件名称修改为 proxy-cache2, 修改后的插件文件列表如下：
删除了内存缓存的相关内容，只保留了磁盘缓存的内容，并添加了一些日志记录好了解整个插件的整体流程。
apisix 添加自定义插件 接下来需要给 apisix 添加我们修改的 proxy-cache2 插件，通过查看容器的目录，我们需要将插件挂载到 /usr/local/apisix/apisix/plugins 目录下，我们修改 docker-compose 文件：
version: "3" services: apisix: image: apache/apisix:${APISIX\_IMAGE\_TAG:-3.2.0-debian} restart: always volumes: - ./apisix\_conf/config.yaml:/usr/local/apisix/conf/config.yaml:ro - ./apisix/plugins/proxy-cache2:/usr/local/apisix/apisix/plugins/proxy-cache2 - ./apisix\_log://usr/local/apisix/logs depends\_on: - etcd ##network\_mode: host ports: - "9180:9180/tcp" - "9080:9080/tcp" - "9091:9091/tcp" - "9443:9443/tcp" - "9092:9092/tcp" networks: apisix: 我们添加 ./apisix/plugins/proxy-cache2:/usr/local/apisix/apisix/plugins/proxy-cache2 将本地的插件目录挂载进行容器中，重启 apisix。
...

 [post link to apisix 如何添加自定义插件](https://jasminides.com/posts/apisix%E5%A6%82%E4%BD%95%E6%B7%BB%E5%8A%A0%E8%87%AA%E5%AE%9A%E4%B9%89%E6%8F%92%E4%BB%B6/)

前言 最近有一个需求，需要配置一个路由，这个路由是子域名形式的，域名类似 xx.apps.overstarry.vip，我们需要根据子域名中的 xx 内容来请求同一个对象存储中不同的文件。
这个需求之前处理过，那时采用了 nginx 来处理主要路径的逻辑，apisix 直接请求 nginx 服务，也就是大概这样的一种结构：apisix -> nginx -> oss。这次同样的需求，我决定采用 2 层结构，去除中间的 nginx 层，由 apisix 直接访问 oss 服务。
接下来我就来讲述处理的过程。
过程 使用 proxy-rewrite 处理这个需求，我第一反应是使用 proxy-rewrite 插件来处理，我使用 regex\_uri 字段来进行正则替换匹配，添加的插件内容如下：
"proxy-rewrite": { "regex\_uri": \[ "^(.\*).apps0.overstarry.vip(.\*)$", "/$1/production$2" \] } 配置完后，请求了几次，发现没有请求成功，通过查看日志发现请求到了奇怪的地址。又仔细的研究了一会，发现是我理解错误了，proxy\_rewrite 是根据 uri 进行正则匹配的，没有根据 host 匹配的选项，前面填写的那些是根本不会匹配成功的。
serverless proxy-rewrite 插件不能实现我们的需求，我又查看了 issue 列表，发现了一个 issue(#7739),里面提到了可以使用插件 serverless 来实现我们的需求。
serverless 介绍 APISIX 有两个 serverless 插件：serverless-pre-function 和 serverless-post-function。
serverless-pre-function 插件会在指定阶段开始时运行，serverless-post-function 插件会在指定阶段结束时运行。这两个插件使用相同的属性。
实现 我们的需求应该是采用 serverless-pre-function 来实现，具体过程描述如下：获得请求的 host, 对 host 进行相应的文本正则替换，将替换的文本和 uri 进行组合拼接，得到真正的 uri.
...

 [post link to apisix 根据请求 host 访问不同路径](https://jasminides.com/posts/apisix%E6%A0%B9%E6%8D%AE%E8%AF%B7%E6%B1%82host%E8%AE%BF%E9%97%AE%E4%B8%8D%E5%90%8C%E8%B7%AF%E5%BE%84/)

前言 最近在给 APISIX 配置自动更新 SSL 证书的时候，发现了一些问题，本文记录以下发现问题的过程和解决方案。
步骤 我们先来看下原始的配置方法吧：
1 安装相应脚本
$ curl --output /root/.acme.sh/renew-hook-update-APISIX.sh --silent https://gist.githubusercontent.com/anjia0532/9ebf8011322f43e3f5037bc2af3aeaa6/raw/65b359a4eed0ae990f9188c2afa22bacd8471652/renew-hook-update-APISIX.sh $ chmod +x /root/.acme.sh/renew-hook-update-APISIX.sh $ /root/.acme.sh/renew-hook-update-APISIX.sh Usage : /root/.acme.sh/renew-hook-update-APISIX.sh -h <APISIX admin host> -p <certificate pem file> -k <certificate private key file> -a <admin api key> -t <print debug info switch off/on,default off> 2 安装 acme.sh
curl https://get.acme.sh \| sh -s email=my@example.com 3 申请证书，并添加 renew-hook
这里我采用的是 dns api 的方式申请证书的
~/.acme.sh/acme.sh --issue --dns dns\_ali -d \*.xx.com --renew-hook '~/.acme.sh/renew-hook-update-APISIX.sh -h http://127.0.0.1:9280 -p ~/.acme.sh/"\*.xx.com\_ecc"/"fullchain.cer" -k ~/.acme.sh/"\*.xx.com\_ecc"/"\*.xx.com.key" -a {admin-key}' --log --debug 这里的 http://127.0.0.1:9280 是你的 APISIX 的 admin 接口地址，admin-key 是你的 key。
...

 [post link to 使用 acme 自动更新 APISIX ssl 证书](https://jasminides.com/posts/%E4%BD%BF%E7%94%A8acme%E8%87%AA%E5%8A%A8%E6%9B%B4%E6%96%B0apisix_ssl%E8%AF%81%E4%B9%A6/)

本文我来讲解如何使用 APISIX 来代理 PostgreSQL 数据库服务。
初试 最开始我以为很简单，我采用了直接在 APISIX DashBoard 上配置了一条路由，配置好后，连接发现无法成功连接，提示连接失败。
经过仔细的思考，发现 PostgreSQL 是使用 TCP 协议的数据库，不能通过简单的 route 进行配置，必须使用 stream-proxy 进行代理，接下来我们来看看怎么样来进行配置。
stream-proxy TCP 是许多流行应用程序和服务的协议，例如 LDAP、MySQL 和 RTMP。UDP（用户数据报协议）是许多流行的非事务性应用程序的协议，例如 DNS、系统日志和 RADIUS。
APISIX 可以动态负载平衡 TCP/UDP 代理。在 Nginx 的世界里，我们把 TCP/UDP proxy 称为 stream proxy，APISIX 就遵循了这个说法。
启用 stream-proxy 要开启 APISIX 流代理需要在 APISIX 配置中开启，APISIX 默认是关闭的。
apisix: stream\_proxy: # TCP/UDP proxy tcp: # TCP proxy address list - 9100 - "127.0.0.1:9101" udp: # UDP proxy address list - 9200 - "127.0.0.1:9211" 如果 apisix.enable\_admin 为 true，则 HTTP 和流代理都启用了上述配置。
...

 [post link to 使用 APISIX 代理 PostgreSQL 数据库](https://jasminides.com/posts/%E4%BD%BF%E7%94%A8apisix%E4%BB%A3%E7%90%86postgresql%E6%9C%8D%E5%8A%A1/)

前言 最近需要使用 apisix 反向代理 oss, 实现通过域名访问相应的资源 (由于条件的限制，不能在 oss 绑定自定义域名)，我直接在 apisix dashboard 配置了路由，创建成功后，我通过浏览器访问时，发现资源不能预览会直接下载。
这样的现象让我很奇怪，通过查阅相关资料，发现使用 OSS 默认域名通过文件 URL 从浏览器访问图片或者网页文件时，Response Header 中会自动加上 Content-Disposition:attachment。即从浏览器访问这些文件时，会以附件形式进行下载。
解决 通过询问同事，得知他是通过 nginx 的 proxy\_hide\_header 忽略 Content-Disposition 解决的。那 apisix 该怎么实现呢，我通过自己的不断尝试和提 issue 询问官方人员，得知可以使用 response-rewrite 插件实现这个功能。
接下来我就来介绍下我尝试的过程吧，我最开始是使用 proxy-rewrite 将 Content-Disposition 设置为 inline，具体配置如下：
{ "uri": "/\*", "name": "xx", "host": "xixi.xx.work", "plugins": { "proxy-rewrite": { "headers": { "Content-Disposition": "inline" }, "host": "xx", "regex\_uri": \[ "/(.\*)$", "/xx/${1}" \] } }, "upstream": { "nodes": \[ { "host": "xxx.com", "port": 80, "weight": 1 } \], "timeout": { "connect": 6, "send": 6, "read": 6 }, "type": "roundrobin", "scheme": "http", "pass\_host": "pass", "keepalive\_pool": { "idle\_timeout": 60, "requests": 1000, "size": 320 } }, "status": 1 } curl 结果：
...

 [post link to apisix 实现 nginx proxy_hide_header 参数](https://jasminides.com/posts/apisix%E5%AE%9E%E7%8E%B0nginx%E7%9A%84proxy_hide_header%E5%8F%82%E6%95%B0/) [Go to Top (Alt + G)](https://jasminides.com/tags/apisix/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fapisix%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801953796&bpp=6&bdt=165&idt=281&shv=r20250319&mjsv=m202503190101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=639047114813&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C31091180%2C31091146%2C95355965&oid=2&pvsid=196840978594556&tmod=1569827671&uas=0&nvt=1&fsapi=1&fc=1920&brdim=330%2C330%2C330%2C330%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=302)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Enable Gzip in Apisix
目录

- [gzip 插件](https://jasminides.com/posts/apisix_enabled_gzip/#gzip-%e6%8f%92%e4%bb%b6)
- [自定义 Nginx 配置](https://jasminides.com/posts/apisix_enabled_gzip/#%e8%87%aa%e5%ae%9a%e4%b9%89-nginx-%e9%85%8d%e7%bd%ae)
- [小结](https://jasminides.com/posts/apisix_enabled_gzip/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/apisix_enabled_gzip/#%e5%8f%82%e8%80%83)

最近使用 Apisix 网关时，需要开启 gzip 功能，通过查阅资料学习，了解了几种开启 gzip 的方式，本文记录 2 种 Apisix 开启 gzip 的方式。

## gzip 插件

我们可以使用 gzip 插件 针对某些路由开启 gzip，只需对路由使用 gzip 插件并配置一些插件属性即可。

![img.png](https://jasminides.com/img/apisix_gzip/img.png)

接下来使用一个例子来演示 gzip 插件，使用 apisix admin api 创建一条路由，要注意的是本文的例子是使用 apisix 3.7 版本：

```shell
curl -i http://127.0.0.1:9180/apisix/admin/routes  \
-H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X POST -d '
{
	"uri": "/get",
	"plugins": {
		"gzip": {
			"buffers": {
				"number": 8
			},
		"comp_level": 6,
		"disable": false,
		"types": "*"
		}
	},
	"upstream": {
    "nodes": [\
      {\
        "host": "httpbin.org",\
        "port": 443,\
        "weight": 1\
      }\
    ],
    "timeout": {
      "connect": 6,
      "send": 6,
      "read": 6
    },
    "type": "roundrobin",
    "scheme": "https",
    "pass_host": "pass",
    "keepalive_pool": {
      "idle_timeout": 60,
      "requests": 1000,
      "size": 320
    }
  },
	"status": 1
}'

```

复制

![img_1.png](https://jasminides.com/img/apisix_gzip/img_1.png)

通过访问链接可以看到插件开启成功了。

![img_2.png](https://jasminides.com/img/apisix_gzip/img_2.png)

接下来介绍另一种方法，自定义 Nginx 配置。

## 自定义 Nginx 配置

接下来介绍另一种方法 自定义 Nginx 配置，这种方法可以针对全局路由开启 gzip。apisix 会通过 apisix/cli/ngx\_tpl.lua 这个模板和 conf/config-default.yaml 加 conf/config.yaml 的配置生成 Nginx 配置文件。

在执行完启动后，你可以在 conf/nginx.conf 看到生成的 Nginx 配置文件。

打开 apisix 的配置文件 conf/config.yaml 文件，添加以下配置 (需要注意原有是否有其它 nginx 配置):

```yaml
  nginx_config:

    http_configuration_snippet: |
      gzip on;
      gzip_http_version 1.1;
      gzip_buffers 256 64k;
      gzip_comp_level 5;
      gzip_min_length 1000;
      gzip_proxied expired no-cache no-store private auth;
      gzip_types application/javascript application/x-javascript text/javascript application/json text/css;
      gzip_disable "MSIE 6";
      gzip_vary on;

```

复制

添加后，访问同样可以看见 gzip 开启。

## 小结

本文介绍了两种为 apisix 开启 gzip 的方式，插件的方式简单快捷但一次只适用于单个路由，nginx 配置的方式麻烦但适合全局路由控制。

## 参考

- [https://apisix.apache.org/docs/apisix/plugins/gzip/](https://apisix.apache.org/docs/apisix/plugins/gzip/)
- [https://apisix.apache.org/docs/apisix/customize-nginx-configuration/](https://apisix.apache.org/docs/apisix/customize-nginx-configuration/)
- [https://github.com/apache/apisix/issues/8995](https://github.com/apache/apisix/issues/8995)
- [https://github.com/apache/apisix/issues/8995](https://github.com/apache/apisix/issues/8995)

giscus

正在加载评论……

[Go to Top (Alt + G)](https://jasminides.com/posts/apisix_enabled_gzip/#top "Go to Top (Alt + G)")

## Enable Gzip in Apisix
最近使用 Apisix 网关时，需要开启 gzip 功能，通过查阅资料学习，了解了几种开启 gzip 的方式，本文记录 2 种 Apisix 开启 gzip 的方式。
gzip 插件 我们可以使用 gzip 插件 针对某些路由开启 gzip，只需对路由使用 gzip 插件并配置一些插件属性即可。
接下来使用一个例子来演示 gzip 插件，使用 apisix admin api 创建一条路由，要注意的是本文的例子是使用 apisix 3.7 版本：
curl -i http://127.0.0.1:9180/apisix/admin/routes \ -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X POST -d ' { "uri": "/get", "plugins": { "gzip": { "buffers": { "number": 8 }, "comp\_level": 6, "disable": false, "types": "\*" } }, "upstream": { "nodes": \[ { "host": "httpbin.org", "port": 443, "weight": 1 } \], "timeout": { "connect": 6, "send": 6, "read": 6 }, "type": "roundrobin", "scheme": "https", "pass\_host": "pass", "keepalive\_pool": { "idle\_timeout": 60, "requests": 1000, "size": 320 } }, "status": 1 }' ...

 [post link to Apisix 开启 gzip](https://jasminides.com/posts/apisix_enabled_gzip/) [Go to Top (Alt + G)](https://jasminides.com/tags/gzip/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fgzip%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801953825&bpp=3&bdt=178&idt=63&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=1058254645267&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C31091181&oid=2&pvsid=3419744188136744&tmod=378980263&uas=0&nvt=1&fsapi=1&fc=1920&brdim=30%2C30%2C30%2C30%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=86)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Nginx and Apisix Configuration
最近使用 Apisix 网关时，需要开启 gzip 功能，通过查阅资料学习，了解了几种开启 gzip 的方式，本文记录 2 种 Apisix 开启 gzip 的方式。
gzip 插件 我们可以使用 gzip 插件 针对某些路由开启 gzip，只需对路由使用 gzip 插件并配置一些插件属性即可。
接下来使用一个例子来演示 gzip 插件，使用 apisix admin api 创建一条路由，要注意的是本文的例子是使用 apisix 3.7 版本：
curl -i http://127.0.0.1:9180/apisix/admin/routes \ -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -X POST -d ' { "uri": "/get", "plugins": { "gzip": { "buffers": { "number": 8 }, "comp\_level": 6, "disable": false, "types": "\*" } }, "upstream": { "nodes": \[ { "host": "httpbin.org", "port": 443, "weight": 1 } \], "timeout": { "connect": 6, "send": 6, "read": 6 }, "type": "roundrobin", "scheme": "https", "pass\_host": "pass", "keepalive\_pool": { "idle\_timeout": 60, "requests": 1000, "size": 320 } }, "status": 1 }' ...

 [post link to Apisix 开启 gzip](https://jasminides.com/posts/apisix_enabled_gzip/)

最近在使用 nginx 反向代理时遇到了一些问题，在本文记录一下问题及相应的解决方法。
问题 1 问题现象 错误日志如下：
: host not found in upstream "xx.xx.vip"in /etc/nginx/conf.d/default.conf:17 nginx: \[emerg\] host not found in upstream "xx.xx.vip”in /etc/nginx/conf.d/default. conf:17 从错误日志可以看出这个问题主要是 nginx 无法解析相应的域名。
解决方法 怎么解决这个问题呢，我们只需添加相应的 dns 服务器即可 resolver 8.8.8.8; 。
问题 2 问题现象 错误日志如下：
2023/07/28 01:35:43 \[error\] 34#34: \*44 SSL\_do\_handshake() failed (SSL: error:14094438:SSL routines:ssl3\_read\_bytes:tlsv1 alert internal error:SSL alert number 80) while SSL handshaking to upstream, client: 172.16.64.75, server: , request: "POST /v1/data/xx/filter HTTP/1.1", upstream: "https://xxxx:443/v1/data/xx/filter", host: "xx.xx.com", referrer: "https://xx.xx.com/user/login" 解决方法 这个问题主要是 https 相关配置的问题，我们只需添加这几行配置即可：
...

 [post link to Nginx 反向代理中出现的问题及解决方法](https://jasminides.com/posts/nginx%E5%8F%8D%E5%90%91%E4%BB%A3%E7%90%86%E9%94%99%E8%AF%AF%E7%9A%84%E9%97%AE%E9%A2%98%E5%8F%8A%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95/)

前言 最近有一个需求，需要配置一个路由，这个路由是子域名形式的，域名类似 xx.apps.overstarry.vip，我们需要根据子域名中的 xx 内容来请求同一个对象存储中不同的文件。
这个需求之前处理过，那时采用了 nginx 来处理主要路径的逻辑，apisix 直接请求 nginx 服务，也就是大概这样的一种结构：apisix -> nginx -> oss。这次同样的需求，我决定采用 2 层结构，去除中间的 nginx 层，由 apisix 直接访问 oss 服务。
接下来我就来讲述处理的过程。
过程 使用 proxy-rewrite 处理这个需求，我第一反应是使用 proxy-rewrite 插件来处理，我使用 regex\_uri 字段来进行正则替换匹配，添加的插件内容如下：
"proxy-rewrite": { "regex\_uri": \[ "^(.\*).apps0.overstarry.vip(.\*)$", "/$1/production$2" \] } 配置完后，请求了几次，发现没有请求成功，通过查看日志发现请求到了奇怪的地址。又仔细的研究了一会，发现是我理解错误了，proxy\_rewrite 是根据 uri 进行正则匹配的，没有根据 host 匹配的选项，前面填写的那些是根本不会匹配成功的。
serverless proxy-rewrite 插件不能实现我们的需求，我又查看了 issue 列表，发现了一个 issue(#7739),里面提到了可以使用插件 serverless 来实现我们的需求。
serverless 介绍 APISIX 有两个 serverless 插件：serverless-pre-function 和 serverless-post-function。
serverless-pre-function 插件会在指定阶段开始时运行，serverless-post-function 插件会在指定阶段结束时运行。这两个插件使用相同的属性。
实现 我们的需求应该是采用 serverless-pre-function 来实现，具体过程描述如下：获得请求的 host, 对 host 进行相应的文本正则替换，将替换的文本和 uri 进行组合拼接，得到真正的 uri.
...

 [post link to apisix 根据请求 host 访问不同路径](https://jasminides.com/posts/apisix%E6%A0%B9%E6%8D%AE%E8%AF%B7%E6%B1%82host%E8%AE%BF%E9%97%AE%E4%B8%8D%E5%90%8C%E8%B7%AF%E5%BE%84/)

前言 最近需要使用 apisix 反向代理 oss, 实现通过域名访问相应的资源 (由于条件的限制，不能在 oss 绑定自定义域名)，我直接在 apisix dashboard 配置了路由，创建成功后，我通过浏览器访问时，发现资源不能预览会直接下载。
这样的现象让我很奇怪，通过查阅相关资料，发现使用 OSS 默认域名通过文件 URL 从浏览器访问图片或者网页文件时，Response Header 中会自动加上 Content-Disposition:attachment。即从浏览器访问这些文件时，会以附件形式进行下载。
解决 通过询问同事，得知他是通过 nginx 的 proxy\_hide\_header 忽略 Content-Disposition 解决的。那 apisix 该怎么实现呢，我通过自己的不断尝试和提 issue 询问官方人员，得知可以使用 response-rewrite 插件实现这个功能。
接下来我就来介绍下我尝试的过程吧，我最开始是使用 proxy-rewrite 将 Content-Disposition 设置为 inline，具体配置如下：
{ "uri": "/\*", "name": "xx", "host": "xixi.xx.work", "plugins": { "proxy-rewrite": { "headers": { "Content-Disposition": "inline" }, "host": "xx", "regex\_uri": \[ "/(.\*)$", "/xx/${1}" \] } }, "upstream": { "nodes": \[ { "host": "xxx.com", "port": 80, "weight": 1 } \], "timeout": { "connect": 6, "send": 6, "read": 6 }, "type": "roundrobin", "scheme": "http", "pass\_host": "pass", "keepalive\_pool": { "idle\_timeout": 60, "requests": 1000, "size": 320 } }, "status": 1 } curl 结果：
...

 [post link to apisix 实现 nginx proxy_hide_header 参数](https://jasminides.com/posts/apisix%E5%AE%9E%E7%8E%B0nginx%E7%9A%84proxy_hide_header%E5%8F%82%E6%95%B0/)

Nginx 搭建静态图片资源服务器 本文介绍使用 Docker Nginx 搭建静态图片资源服务器的过程和搭建中间遇到的问题。
我使用 Docker compose 搭建静态图片资源服务器，我使用的 compose 文件内容如下：
version: '3.1' services: nginx: restart: always image: nginx container\_name: asset ports: - 80:80 volumes: - ./nginx.conf:/etc/nginx/nginx.conf - ./uploads:/usr/share/nginx/uploads - ./conf.d:/etc/nginx/conf.d /srv/msg/storage/uploads:/usr/share/nginx/uploads 将本地的图片文件夹挂载到容器内的 /usr/share/nginx/uploads 文件夹 nginx.conf 是 Nginx 的主配置文件，conf.d 是各个网站配置的文件夹。我的 nginx.conf 内容如下：
user nginx; worker\_processes 1; error\_log /var/log/nginx/error.log warn; pid /var/run/nginx.pid; events { worker\_connections 1024; } http { include /etc/nginx/mime.types; default\_type application/octet-stream; log\_format main '$remote\_addr - $remote\_user \[$time\_local\] "$request" ' '$status $body\_bytes\_sent "$http\_referer" ' '"$http\_user\_agent" "$http\_x\_forwarded\_for"'; access\_log /var/log/nginx/access.log main; sendfile on; #tcp\_nopush on; keepalive\_timeout 65; include /etc/nginx/conf.d/\*.conf; server { listen 80 default\_server; listen \[::\]:80 default\_server; server\_name 192.168.1.117; root /usr/share/nginx/uploads/; location /{ autoindex on; } error\_page 404 /404.html; location = /40x.html { } error\_page 500 502 503 504 /50x.html; location = /50x.html { } } } 静态资源图片服务器的配置文件如下：
...

 [post link to Nginx 搭建静态图片资源服务器](https://jasminides.com/posts/nginx%E6%90%AD%E5%BB%BA%E9%9D%99%E6%80%81%E5%9B%BE%E7%89%87%E8%B5%84%E6%BA%90%E6%9C%8D%E5%8A%A1%E5%99%A8/) [Go to Top (Alt + G)](https://jasminides.com/tags/nginx/#top "Go to Top (Alt + G)")

## System Crash Memory Dumps
前言 最近出现了多次因为各种原因导致的操作系统宕机的问题，为了查找系统宕机的原因，需要收集系统宕机后的内存转储信息。本文就介绍几种常见的方式。
阿里云内置命令收集 由于主要使用的是阿里云的服务器，就先介绍阿里云收集系统宕机内存转储信息的方式。
阿里云系统默认没有开启 dump 配置，我们需要使用以下命令开启：acs-plugin-manager --exec --plugin=ecs\_dump\_collector --params="--enable"
那我们如何收集内存转储信息呢，执行以下命令：acs-plugin-manager --exec --plugin=ecs\_dump\_collector --params="-c" 出现以下信息表示收集成功。
有了转储信息文件我们就可以将文件交给专业的运维人员或阿里云工程师进行宕机原因分析。
使用 Crash + Kdump 如果我们没有使用阿里云的服务该如何收集系统崩溃的转储信息呢，我们可以使用 Crash + Kdump 进行收集，通过前面的使用可以看出阿里云的插件就是使用了这两个工具，接下来开始进行简单的介绍。
安装 需要先安装 Crash + Kdump，使用此命令进行安装：
$ sudo apt install linux-crashdump $ sudo apt install crash 安装完为了使服务生效需要重启服务器。
使用以下命令：sudo cat /etc/default/grub.d/kdump-tools.cfg
可以看出系统保留了 192M RAM 内存区供转储捕获内核使用
收集 为了测试方便我们可以使用此命令快速触发崩溃：sudo echo c > /proc/sysrq-trigger 。命令执行后在 /var/crash 目录会生成以当前时间为名称的目录，目录里面就是收集到的转储信息。
demsg.x 为崩溃时候的系统内核日志，dump.x 文件则为转储的内核快照文件。为了更好的查找问题，我们还需要安装 vmlinux，使用以下命令安装：
...

 [post link to 如何收集系统宕机后的内存转储信息](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/) [Go to Top (Alt + G)](https://jasminides.com/tags/crash/#top "Go to Top (Alt + G)")

## System Crash Memory Dump
前言 最近出现了多次因为各种原因导致的操作系统宕机的问题，为了查找系统宕机的原因，需要收集系统宕机后的内存转储信息。本文就介绍几种常见的方式。
阿里云内置命令收集 由于主要使用的是阿里云的服务器，就先介绍阿里云收集系统宕机内存转储信息的方式。
阿里云系统默认没有开启 dump 配置，我们需要使用以下命令开启：acs-plugin-manager --exec --plugin=ecs\_dump\_collector --params="--enable"
那我们如何收集内存转储信息呢，执行以下命令：acs-plugin-manager --exec --plugin=ecs\_dump\_collector --params="-c" 出现以下信息表示收集成功。
有了转储信息文件我们就可以将文件交给专业的运维人员或阿里云工程师进行宕机原因分析。
使用 Crash + Kdump 如果我们没有使用阿里云的服务该如何收集系统崩溃的转储信息呢，我们可以使用 Crash + Kdump 进行收集，通过前面的使用可以看出阿里云的插件就是使用了这两个工具，接下来开始进行简单的介绍。
安装 需要先安装 Crash + Kdump，使用此命令进行安装：
$ sudo apt install linux-crashdump $ sudo apt install crash 安装完为了使服务生效需要重启服务器。
使用以下命令：sudo cat /etc/default/grub.d/kdump-tools.cfg
可以看出系统保留了 192M RAM 内存区供转储捕获内核使用
收集 为了测试方便我们可以使用此命令快速触发崩溃：sudo echo c > /proc/sysrq-trigger 。命令执行后在 /var/crash 目录会生成以当前时间为名称的目录，目录里面就是收集到的转储信息。
demsg.x 为崩溃时候的系统内核日志，dump.x 文件则为转储的内核快照文件。为了更好的查找问题，我们还需要安装 vmlinux，使用以下命令安装：
...

 [post link to 如何收集系统宕机后的内存转储信息](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/) [Go to Top (Alt + G)](https://jasminides.com/tags/os/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fos%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801953837&bpp=2&bdt=176&idt=154&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=941362466731&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95353451%2C95354563&oid=2&pvsid=1894215640691668&tmod=970260024&uas=0&nvt=1&fsapi=1&fc=1920&brdim=160%2C160%2C160%2C160%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=178)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Ubuntu Memory Dump Guide
前言 最近出现了多次因为各种原因导致的操作系统宕机的问题，为了查找系统宕机的原因，需要收集系统宕机后的内存转储信息。本文就介绍几种常见的方式。
阿里云内置命令收集 由于主要使用的是阿里云的服务器，就先介绍阿里云收集系统宕机内存转储信息的方式。
阿里云系统默认没有开启 dump 配置，我们需要使用以下命令开启：acs-plugin-manager --exec --plugin=ecs\_dump\_collector --params="--enable"
那我们如何收集内存转储信息呢，执行以下命令：acs-plugin-manager --exec --plugin=ecs\_dump\_collector --params="-c" 出现以下信息表示收集成功。
有了转储信息文件我们就可以将文件交给专业的运维人员或阿里云工程师进行宕机原因分析。
使用 Crash + Kdump 如果我们没有使用阿里云的服务该如何收集系统崩溃的转储信息呢，我们可以使用 Crash + Kdump 进行收集，通过前面的使用可以看出阿里云的插件就是使用了这两个工具，接下来开始进行简单的介绍。
安装 需要先安装 Crash + Kdump，使用此命令进行安装：
$ sudo apt install linux-crashdump $ sudo apt install crash 安装完为了使服务生效需要重启服务器。
使用以下命令：sudo cat /etc/default/grub.d/kdump-tools.cfg
可以看出系统保留了 192M RAM 内存区供转储捕获内核使用
收集 为了测试方便我们可以使用此命令快速触发崩溃：sudo echo c > /proc/sysrq-trigger 。命令执行后在 /var/crash 目录会生成以当前时间为名称的目录，目录里面就是收集到的转储信息。
demsg.x 为崩溃时候的系统内核日志，dump.x 文件则为转储的内核快照文件。为了更好的查找问题，我们还需要安装 vmlinux，使用以下命令安装：
...

 [post link to 如何收集系统宕机后的内存转储信息](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/)

最近一台 Ubuntu 出现了网络问题，ping baidu.com 出现了 temporary failure in name resolution 报错，根据我的经验这是服务器的 DNS 出现了问题，特此在本文记录一下如何设置 DNS 的过程。
修改 netplan 配置文件 我先尝试修改 netplan 的配置文件，编辑相应的配置文件，我这里的路径是 /etc/netplan/00-installer-config.yaml, 修改后的内容如下：
network: ethernets: ens160: addresses: - 192.168.1.51/24 gateway4: 192.168.1.1 nameservers: addresses: - 114.114.114.114 search: \[\] version: 2 修改后执行 netplan apply, 重新 ping 后发现没有效果，未能解决问题。
修改 /etc/resolv.conf 我们还可以通过修改 /etc/resolv.conf 文件来设置 dns, 虽然通过修改此文件可以解决我们的问题，但编辑 /etc/resolv.conf 文件时，发现了一行注释 This file is managed by man:systemd-resolved(8). Do not edit. 可以得知这个文件是由 man:systemd-resolved(8) 管理，/etc/resolv.conf 是一个动态生成的文件，下次重启服务器时此文件还会恢复到默认的内容，所以此方案只适合临时解决，不能一次性解决问题。
接下来我来介绍如何永久的修改 /etc/resolv.conf
修改 /etc/systemd/resolved.conf 文件 # This file is part of systemd. # # systemd is free software; you can redistribute it and/or modify it # under the terms of the GNU Lesser General Public License as published by # the Free Software Foundation; either version 2.1 of the License, or # (at your option) any later version. # # Entries in this file show the compile time defaults. # You can change settings by editing this file. # Defaults can be restored by simply deleting this file. # # See resolved.conf(5) for details \[Resolve\] DNS=114.114.114.114 8.8.8.8 #FallbackDNS= #Domains= #LLMNR=no #MulticastDNS=no #DNSSEC=no #DNSOverTLS=no #Cache=no-negative #DNSStubListener=yes #ReadEtcHosts=yes ~ ~ ~ ~ ~ ~ ~ 添加要修改的 dns 信息。
...

 [post link to Ubuntu20.04 设置 DNS](https://jasminides.com/posts/ubuntu20.04%E8%AE%BE%E7%BD%AEdns/) [Go to Top (Alt + G)](https://jasminides.com/tags/ubuntu/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fubuntu%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801958806&bpp=5&bdt=478&idt=385&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=3823115217704&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95332924%2C95353387%2C95353450&oid=2&pvsid=130464556703703&tmod=889701955&uas=0&nvt=1&fsapi=1&fc=1920&brdim=190%2C190%2C190%2C190%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=460)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Memory Dump Collection Guide
前言 最近出现了多次因为各种原因导致的操作系统宕机的问题，为了查找系统宕机的原因，需要收集系统宕机后的内存转储信息。本文就介绍几种常见的方式。
阿里云内置命令收集 由于主要使用的是阿里云的服务器，就先介绍阿里云收集系统宕机内存转储信息的方式。
阿里云系统默认没有开启 dump 配置，我们需要使用以下命令开启：acs-plugin-manager --exec --plugin=ecs\_dump\_collector --params="--enable"
那我们如何收集内存转储信息呢，执行以下命令：acs-plugin-manager --exec --plugin=ecs\_dump\_collector --params="-c" 出现以下信息表示收集成功。
有了转储信息文件我们就可以将文件交给专业的运维人员或阿里云工程师进行宕机原因分析。
使用 Crash + Kdump 如果我们没有使用阿里云的服务该如何收集系统崩溃的转储信息呢，我们可以使用 Crash + Kdump 进行收集，通过前面的使用可以看出阿里云的插件就是使用了这两个工具，接下来开始进行简单的介绍。
安装 需要先安装 Crash + Kdump，使用此命令进行安装：
$ sudo apt install linux-crashdump $ sudo apt install crash 安装完为了使服务生效需要重启服务器。
使用以下命令：sudo cat /etc/default/grub.d/kdump-tools.cfg
可以看出系统保留了 192M RAM 内存区供转储捕获内核使用
收集 为了测试方便我们可以使用此命令快速触发崩溃：sudo echo c > /proc/sysrq-trigger 。命令执行后在 /var/crash 目录会生成以当前时间为名称的目录，目录里面就是收集到的转储信息。
demsg.x 为崩溃时候的系统内核日志，dump.x 文件则为转储的内核快照文件。为了更好的查找问题，我们还需要安装 vmlinux，使用以下命令安装：
...

 [post link to 如何收集系统宕机后的内存转储信息](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/) [Go to Top (Alt + G)](https://jasminides.com/tags/%E9%98%BF%E9%87%8C%E4%BA%91/#top "Go to Top (Alt + G)")

## Memory Dump Collection
目录

- [前言](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/#%e5%89%8d%e8%a8%80)
- [阿里云内置命令收集](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/#%e9%98%bf%e9%87%8c%e4%ba%91%e5%86%85%e7%bd%ae%e5%91%bd%e4%bb%a4%e6%94%b6%e9%9b%86)
- [使用 Crash + Kdump](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/#%e4%bd%bf%e7%94%a8-crash--kdump)
  - [安装](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/#%e5%ae%89%e8%a3%85)
  - [收集](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/#%e6%94%b6%e9%9b%86)
- [参考](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/#%e5%8f%82%e8%80%83)

## 前言

最近出现了多次因为各种原因导致的操作系统宕机的问题，为了查找系统宕机的原因，需要收集系统宕机后的内存转储信息。本文就介绍几种常见的方式。

## 阿里云内置命令收集

由于主要使用的是阿里云的服务器，就先介绍阿里云收集系统宕机内存转储信息的方式。

阿里云系统默认没有开启 dump 配置，我们需要使用以下命令开启： `acs-plugin-manager --exec --plugin=ecs_dump_collector --params="--enable"`

![img.png](https://jasminides.com/img/crash/img.png)

那我们如何收集内存转储信息呢，执行以下命令： `acs-plugin-manager --exec --plugin=ecs_dump_collector --params="-c"` 出现以下信息表示收集成功。

![img_1.png](https://jasminides.com/img/crash/img_1.png)

![img_2.png](https://jasminides.com/img/crash/img_2.png)

有了转储信息文件我们就可以将文件交给专业的运维人员或阿里云工程师进行宕机原因分析。

## 使用 Crash + Kdump

如果我们没有使用阿里云的服务该如何收集系统崩溃的转储信息呢，我们可以使用 Crash + Kdump 进行收集，通过前面的使用可以看出阿里云的插件就是使用了这两个工具，接下来开始进行简单的介绍。

### 安装

需要先安装 Crash + Kdump，使用此命令进行安装：

```shell
$ sudo apt install linux-crashdump
$ sudo apt install crash

```

复制

安装完为了使服务生效需要重启服务器。

使用以下命令： `sudo cat /etc/default/grub.d/kdump-tools.cfg`

![img_3.png](https://jasminides.com/img/crash/img_3.png)![img_4.png](https://jasminides.com/img/crash/img_4.png)

可以看出系统保留了 192M RAM 内存区供转储捕获内核使用

### 收集

为了测试方便我们可以使用此命令快速触发崩溃： `sudo echo c > /proc/sysrq-trigger` 。命令执行后在 /var/crash 目录会生成以当前时间为名称的目录，目录里面就是收集到的转储信息。

![img_5.png](https://jasminides.com/img/crash/img_5.png)

demsg.x 为崩溃时候的系统内核日志，dump.x 文件则为转储的内核快照文件。为了更好的查找问题，我们还需要安装 vmlinux，使用以下命令安装：

```shell
echo "deb http://ddebs.ubuntu.com $(lsb_release -cs) main restricted universe multiverse
 deb http://ddebs.ubuntu.com $(lsb_release -cs)-updates main restricted universe multiverse
 deb http://ddebs.ubuntu.com $(lsb_release -cs)-proposed main restricted universe multiverse" | sudo tee -a /etc/apt/sources.list.d/ddebs.list
 sudo apt install ubuntu-dbgsym-keyring
sudo apt-get update
sudo apt -y install linux-image-$(uname -r)-dbgsym

```

复制

安装完我们就可以对刚刚收集到的转储文件进行分析了，使用命令：

```shell
sudo crash /usr/lib/debug/boot/vmlinux-5.4.0-166-generic /var/crash/202401061626/dump.202401061626

```

复制

输出：

```console
crash 7.2.8
Copyright (C) 2002-2020  Red Hat, Inc.
Copyright (C) 2004, 2005, 2006, 2010  IBM Corporation
Copyright (C) 1999-2006  Hewlett-Packard Co
Copyright (C) 2005, 2006, 2011, 2012  Fujitsu Limited
Copyright (C) 2006, 2007  VA Linux Systems Japan K.K.
Copyright (C) 2005, 2011  NEC Corporation
Copyright (C) 1999, 2002, 2007  Silicon Graphics, Inc.
Copyright (C) 1999, 2000, 2001, 2002  Mission Critical Linux, Inc.
This program is free software, covered by the GNU General Public License,
and you are welcome to change it and/or distribute copies of it under
certain conditions.  Enter "help copying" to see the conditions.
This program has absolutely no warranty.  Enter "help warranty" for details.

GNU gdb (GDB) 7.6
Copyright (C) 2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-unknown-linux-gnu"...

WARNING: kernel relocated [300MB]: patching 115314 gdb minimal_symbol values

      KERNEL: /usr/lib/debug/boot/vmlinux-5.4.0-166-generic
    DUMPFILE: /var/crash/202401061626/dump.202401061626  [PARTIAL DUMP]
        CPUS: 2
        DATE: Sat Jan  6 16:26:23 2024
      UPTIME: 00:06:35
LOAD AVERAGE: 0.00, 0.02, 0.02
       TASKS: 148
    NODENAME: iZ7xv1a0t15muqy1e2co1uZ
     RELEASE: 5.4.0-166-generic
     VERSION: #183-Ubuntu SMP Mon Oct 2 11:28:33 UTC 2023
     MACHINE: x86_64  (2699 Mhz)
      MEMORY: 3.9 GB
       PANIC: "Kernel panic - not syncing: sysrq triggered crash"
         PID: 3654
     COMMAND: "echo"
        TASK: ffff8c4a696d8000  [THREAD_INFO: ffff8c4a696d8000]
         CPU: 0
       STATE: TASK_RUNNING (PANIC)

```

复制

使用 bt 命令查看崩溃时的调用栈：

```console
crash> bt
PID: 3654   TASK: ffff8c4a696d8000  CPU: 0   COMMAND: "echo"
 #0 [ffffabde00513c68] machine_kexec at ffffffff93c6d063
 #1 [ffffabde00513cc8] __crash_kexec at ffffffff93d4de32
 #2 [ffffabde00513d98] panic at ffffffff946a69a8
 #3 [ffffabde00513e18] sysrq_handle_crash at ffffffff94288205
 #4 [ffffabde00513e28] __handle_sysrq.cold at ffffffff946ce885
 #5 [ffffabde00513e60] write_sysrq_trigger at ffffffff94288a38
 #6 [ffffabde00513e78] proc_reg_write at ffffffff93f69113
 #7 [ffffabde00513e98] __vfs_write at ffffffff93ed1b6b
 #8 [ffffabde00513ea8] vfs_write at ffffffff93ed2879
 #9 [ffffabde00513ee0] ksys_write at ffffffff93ed4e07
#10 [ffffabde00513f20] __x64_sys_write at ffffffff93ed4e9a
#11 [ffffabde00513f30] do_syscall_64 at ffffffff93c04fe7
#12 [ffffabde00513f50] entry_SYSCALL_64_after_hwframe at ffffffff948000a4
    RIP: 00007ff833b41077  RSP: 00007ffeadb56b78  RFLAGS: 00000246
    RAX: ffffffffffffffda  RBX: 0000000000000002  RCX: 00007ff833b41077
    RDX: 0000000000000002  RSI: 000055b3e2648440  RDI: 0000000000000001
    RBP: 000055b3e2648440   R8: 0000000000000000   R9: 0000000000000001
    R10: 00007ff833c1c640  R11: 0000000000000246  R12: 0000000000000002
    R13: 00007ff833c206a0  R14: 00007ff833c1c4a0  R15: 00007ff833c1b8a0
    ORIG_RAX: 0000000000000001  CS: 0033  SS: 002b

```

复制

crash 还有很多用法，感兴趣的读者可以自行研究学习。

## 参考

- [https://help.aliyun.com/zh/ecs/user-guide/collect-kdump-information-after-an-instance-experiences-an-operating-system-failure?spm=5176.smartservice\_service\_robot\_chat\_new.0.0.aedc3f1bqtn8Zi](https://help.aliyun.com/zh/ecs/user-guide/collect-kdump-information-after-an-instance-experiences-an-operating-system-failure?spm=5176.smartservice_service_robot_chat_new.0.0.aedc3f1bqtn8Zi)
- [https://crash-utility.github.io/crash\_whitepaper.html#WHY\_CRASH](https://crash-utility.github.io/crash_whitepaper.html#WHY_CRASH)

[Go to Top (Alt + G)](https://jasminides.com/posts/%E5%A6%82%E4%BD%95%E6%94%B6%E9%9B%86%E7%B3%BB%E7%BB%9F%E5%AE%95%E6%9C%BA%E5%90%8E%E7%9A%84%E5%86%85%E5%AD%98%E8%BD%AC%E5%82%A8%E4%BF%A1%E6%81%AF/#top "Go to Top (Alt + G)")

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

## Chinese to Pinyin
目录

- [前言](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/#%e5%89%8d%e8%a8%80)
- [安装](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/#%e5%ae%89%e8%a3%85)
  - [cli 安装](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/#cli-%e5%ae%89%e8%a3%85)
- [使用](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/#%e4%bd%bf%e7%94%a8)
  - [cli 使用](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/#cli-%e4%bd%bf%e7%94%a8)
  - [api 使用](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/#api-%e4%bd%bf%e7%94%a8)
- [小结](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/#%e5%8f%82%e8%80%83)

## 前言

本文介绍一个 go 汉字转拼音的库 go-pinyin，可以从名字看出这个库的功能就是将汉字转换为相应的拼音。接下来就由我来简单的介绍 go-pinyin。

## 安装

使用此命令安装： `go get github.com/mozillazg/go-pinyin`

### cli 安装

如果你的 go 版本在 1.17 以下使用此命令安装： `go get -u github.com/mozillazg/go-pinyin/cli/pinyin`。1.17 及以上版本使用此命令安装： `go install github.com/mozillazg/go-pinyin/cli/pinyin@latest`。

## 使用

接下来将分别介绍 cli 的使用和 API 的使用。

### cli 使用

安装完在终端输入 pinyin，可以看到使用的方法，尝试一个汉字，可以看到相应的拼音，但也可以看出对多音字的支持有问题。
![img.png](https://jasminides.com/img/pinyin/img.png)

```console
$ pinyin 中国
zhōng guó
$ pinyin 重庆
zhòng qìng

```

复制

接下来介绍 API 的使用。

### api 使用

通过查看文档，可以看出主要是 2 个方法 `pinyin.NewArgs` 和 `pinyin.Pinyin` 。

`pinyin.NewArgs` 创建包含默认配置的 Args, 可以通过修改 Args 的成员来使用不同的模式。

```go
type Args struct {
	Style     int    // 拼音风格（默认：Normal)
	Heteronym bool   // 是否启用多音字模式（默认：禁用）
	Separator string // Slug 中使用的分隔符（默认：-)

	// 处理没有拼音的字符（默认忽略没有拼音的字符）
	// 函数返回的 slice 的长度为 0 则表示忽略这个字符
	Fallback func(r rune, a Args) []string
}

```

复制

`pinyin.Pinyin` 就是将汉字转为拼音。

接下来看一个简单的例子：

```go
package main

import (
	"fmt"
	"github.com/mozillazg/go-pinyin"
)

func main() {
	hans := "福建"

	// 默认
	a := pinyin.NewArgs()
	fmt.Println(pinyin.Pinyin(hans, a))

	// 包含声调
	a.Style = pinyin.Tone
	fmt.Println(pinyin.Pinyin(hans, a))

	// 声调用数字表示
	a.Style = pinyin.Tone2
	fmt.Println(pinyin.Pinyin(hans, a))
	hans = "重庆"
	// 开启多音字模式
	a = pinyin.NewArgs()
	a.Heteronym = true
	fmt.Println(pinyin.Pinyin(hans, a))
	a.Style = pinyin.Tone2
	fmt.Println(pinyin.Pinyin(hans, a))

}

```

复制

输出：

```console
[[fu] [jian]]
[[fú] [jiàn]]
[[fu2] [jia4n]]
[[zhong chong tong] [qing]]
[[zho4ng cho2ng to2ng] [qi4ng]]

```

复制

通过结果可以看出对多音字的支持有问题。

## 小结

本文简单介绍了 go 中的中文转拼音的库 go-pinyin，通过对库的使用，可以发现词库对多音字的支持有问题，但一些常规的支持还是很完善的。

## 参考

- [https://github.com/mozillazg/pinyin-data](https://github.com/mozillazg/pinyin-data)
- [https://github.com/mozillazg/go-pinyin](https://github.com/mozillazg/go-pinyin)

giscus

正在加载评论……

[Go to Top (Alt + G)](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/#top "Go to Top (Alt + G)")

## Go Pinyin Library Guide
前言 本文介绍一个 go 汉字转拼音的库 go-pinyin，可以从名字看出这个库的功能就是将汉字转换为相应的拼音。接下来就由我来简单的介绍 go-pinyin。
安装 使用此命令安装：go get github.com/mozillazg/go-pinyin
cli 安装 如果你的 go 版本在 1.17 以下使用此命令安装：go get -u github.com/mozillazg/go-pinyin/cli/pinyin。1.17 及以上版本使用此命令安装：go install github.com/mozillazg/go-pinyin/cli/pinyin@latest。
使用 接下来将分别介绍 cli 的使用和 API 的使用。
cli 使用 安装完在终端输入 pinyin，可以看到使用的方法，尝试一个汉字，可以看到相应的拼音，但也可以看出对多音字的支持有问题。 $ pinyin 中国 zhōng guó $ pinyin 重庆 zhòng qìng 接下来介绍 API 的使用。
api 使用 通过查看文档，可以看出主要是 2 个方法 pinyin.NewArgs 和 pinyin.Pinyin 。
pinyin.NewArgs 创建包含默认配置的 Args, 可以通过修改 Args 的成员来使用不同的模式。
type Args struct { Style int // 拼音风格（默认：Normal) Heteronym bool // 是否启用多音字模式（默认：禁用） Separator string // Slug 中使用的分隔符（默认：-) // 处理没有拼音的字符（默认忽略没有拼音的字符） // 函数返回的 slice 的长度为 0 则表示忽略这个字符 Fallback func(r rune, a Args) \[\]string } pinyin.Pinyin 就是将汉字转为拼音。
...

 [post link to go 汉字转拼音 go-pinyin](https://jasminides.com/posts/conversion_of_chinese_characters_into_pinyin/) [Go to Top (Alt + G)](https://jasminides.com/tags/text/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Ftext%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801958257&bpp=2&bdt=194&idt=106&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=18234430685&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C31091180%2C31091145%2C95355301&oid=2&pvsid=2701190227225179&tmod=1551675337&uas=0&nvt=1&fsapi=1&fc=1920&brdim=160%2C160%2C160%2C160%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=145)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Mergo Library Overview
前言 今天介绍一个 go 库 - mergo, mergo 用来方便的合并 struct 和 map ,可以将结构体的字段赋值到 map 中，可以将 map 的值赋值给结构体的字段。
Mergo 通过在零值字段中设置默认值来合并同类型的 struct 和 map。Mergo 不会合并未导出（私有）字段。它会递归合并任何已导出的字段。它也不会合并 map 中的结构体（因为它们无法使用 Go 反射寻址）。
Mergo 在很多知名项目中被使用，如 containerd、k8s、loki 等。
安装 使用以下命令安装 mergo : go get -u dario.cat/mergo
使用 接下来介绍 mergo 的基础使用和高级用法。
基础使用 mergo 提供了 2 个主要函数：Merge 和 Map, Mergo 用来合并 2 个相同结构的 struct 和 map, Map 用来在结构和 map 之间赋值。
例子：
package main import ( "fmt" "log" "github.com/imdario/mergo" ) type redisConfig struct { Address string Port int DB int UserName string PassWord string } var defaultConfig = redisConfig{ Address: "127.0.0.1", Port: 6379, DB: 1, UserName: "123", PassWord: "123", } func main() { var config redisConfig if err := mergo.Merge(&config, defaultConfig); err != nil { log.Fatal(err) } fmt.Println("redis address: ", config.Address) fmt.Println("redis port: ", config.Port) fmt.Println("redis db: ", config.DB) fmt.Println("redis username: ", config.UserName) fmt.Println("redis password: ", config.PassWord) var m = make(map\[string\]interface{}) if err := mergo.Map(&m, defaultConfig); err != nil { log.Fatal(err) } fmt.Println(m) } 接下来介绍一些高级用法：
...

 [post link to mergo 介绍](https://jasminides.com/posts/mergo_desc/) [Go to Top (Alt + G)](https://jasminides.com/tags/mapping/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fmapping%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801958164&bpp=2&bdt=194&idt=132&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=7350120602835&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95344789%2C95355964%2C95355301&oid=2&pvsid=3145025855185972&tmod=640904773&uas=0&nvt=1&fsapi=1&fc=1920&brdim=470%2C470%2C470%2C470%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=148)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Mergo Library Overview
前言 今天介绍一个 go 库 - mergo, mergo 用来方便的合并 struct 和 map ,可以将结构体的字段赋值到 map 中，可以将 map 的值赋值给结构体的字段。
Mergo 通过在零值字段中设置默认值来合并同类型的 struct 和 map。Mergo 不会合并未导出（私有）字段。它会递归合并任何已导出的字段。它也不会合并 map 中的结构体（因为它们无法使用 Go 反射寻址）。
Mergo 在很多知名项目中被使用，如 containerd、k8s、loki 等。
安装 使用以下命令安装 mergo : go get -u dario.cat/mergo
使用 接下来介绍 mergo 的基础使用和高级用法。
基础使用 mergo 提供了 2 个主要函数：Merge 和 Map, Mergo 用来合并 2 个相同结构的 struct 和 map, Map 用来在结构和 map 之间赋值。
例子：
package main import ( "fmt" "log" "github.com/imdario/mergo" ) type redisConfig struct { Address string Port int DB int UserName string PassWord string } var defaultConfig = redisConfig{ Address: "127.0.0.1", Port: 6379, DB: 1, UserName: "123", PassWord: "123", } func main() { var config redisConfig if err := mergo.Merge(&config, defaultConfig); err != nil { log.Fatal(err) } fmt.Println("redis address: ", config.Address) fmt.Println("redis port: ", config.Port) fmt.Println("redis db: ", config.DB) fmt.Println("redis username: ", config.UserName) fmt.Println("redis password: ", config.PassWord) var m = make(map\[string\]interface{}) if err := mergo.Map(&m, defaultConfig); err != nil { log.Fatal(err) } fmt.Println(m) } 接下来介绍一些高级用法：
...

 [post link to mergo 介绍](https://jasminides.com/posts/mergo_desc/) [Go to Top (Alt + G)](https://jasminides.com/tags/mergo/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fmergo%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801958288&bpp=3&bdt=244&idt=147&shv=r20250319&mjsv=m202503200101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=274636558114&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C31091179%2C95340253%2C95340255&oid=2&pvsid=317097203570054&tmod=1859242128&uas=0&nvt=1&fsapi=1&fc=1920&brdim=100%2C100%2C100%2C100%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=174)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Mergo Library Guide
目录

- [前言](https://jasminides.com/posts/mergo_desc/#%e5%89%8d%e8%a8%80)
- [安装](https://jasminides.com/posts/mergo_desc/#%e5%ae%89%e8%a3%85)
- [使用](https://jasminides.com/posts/mergo_desc/#%e4%bd%bf%e7%94%a8)
  - [基础使用](https://jasminides.com/posts/mergo_desc/#%e5%9f%ba%e7%a1%80%e4%bd%bf%e7%94%a8)
  - [覆盖](https://jasminides.com/posts/mergo_desc/#%e8%a6%86%e7%9b%96)
  - [slice](https://jasminides.com/posts/mergo_desc/#slice)
- [小结](https://jasminides.com/posts/mergo_desc/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/mergo_desc/#%e5%8f%82%e8%80%83)

## 前言

今天介绍一个 go 库 - mergo, mergo 用来方便的合并 struct 和 map ,可以将结构体的字段赋值到 map 中，可以将 map 的值赋值给结构体的字段。

Mergo 通过在零值字段中设置默认值来合并同类型的 struct 和 map。Mergo 不会合并未导出（私有）字段。它会递归合并任何已导出的字段。它也不会合并 map 中的结构体（因为它们无法使用 Go 反射寻址）。

Mergo 在很多知名项目中被使用，如 containerd、k8s、loki 等。

## 安装

使用以下命令安装 mergo : `go get -u dario.cat/mergo`

## 使用

接下来介绍 mergo 的基础使用和高级用法。

### 基础使用

mergo 提供了 2 个主要函数：Merge 和 Map, Mergo 用来合并 2 个相同结构的 struct 和 map, Map 用来在结构和 map 之间赋值。

例子：

```go
package main

import (
	"fmt"
	"log"

	"github.com/imdario/mergo"
)

type redisConfig struct {
	Address  string
	Port     int
	DB       int
	UserName string
	PassWord string
}

var defaultConfig = redisConfig{
	Address:  "127.0.0.1",
	Port:     6379,
	DB:       1,
	UserName: "123",
	PassWord: "123",
}

func main() {
	var config redisConfig

	if err := mergo.Merge(&config, defaultConfig); err != nil {
		log.Fatal(err)
	}

	fmt.Println("redis address: ", config.Address)
	fmt.Println("redis port: ", config.Port)
	fmt.Println("redis db: ", config.DB)
	fmt.Println("redis username: ", config.UserName)
	fmt.Println("redis password: ", config.PassWord)

	var m = make(map[string]interface{})
	if err := mergo.Map(&m, defaultConfig); err != nil {
		log.Fatal(err)
	}

	fmt.Println(m)
}

```

复制

接下来介绍一些高级用法：

### 覆盖

如果目标结构已经有初始值的情况，Merge/Map 函数不会覆盖已经有的值，如果想要覆盖原有的值，需要使用 `WithOverride` 参数。

```go
	var config redisConfig
	config.UserName = "overstarry"
	if err := mergo.Merge(&config, defaultConfig, mergo.WithOverride); err != nil {
		log.Fatal(err)
	}

```

复制

如果需要检查合并的对象类型是否一致，可以使用 `mergo.WithTypeCheck` 参数。如果需要覆盖指针，则需使用 `WithoutDereference` 参数。

### slice

如果结构体中的字段是切片类型，覆盖时想要合并 2 个切片，则使用 `WithAppendSlice` 参数。

```go
  if err := mergo.Merge(&config, defaultConfig, mergo.WithAppendSlice); err != nil {
    log.Fatal(err)
  }

```

复制

## 小结

本文简单的介绍了 mergo 库和常用的一些参数用法，mergo 还提供了一些复杂的参数，有兴趣的读者可以自行研究。

## 参考

- [https://github.com/darccio/mergo](https://github.com/darccio/mergo)
- [https://pkg.go.dev/github.com/imdario/mergo?utm\_source=godoc](https://pkg.go.dev/github.com/imdario/mergo?utm_source=godoc)

[Go to Top (Alt + G)](https://jasminides.com/posts/mergo_desc/#top "Go to Top (Alt + G)")

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

## Better Go Concurrency
前言 本文介绍 conc - 一个更好的 go 并发库，sourcegraph 在日常开发中使用 go 原生并发出现了问题，由此开发了 conc，相比标准并发代码更优雅，代码更少，下面展示一个例子，可以看出代码减少了许多。
type propagatedPanic struct { val any stack \[\]byte } func main() { done := make(chan \*propagatedPanic) go func() { defer func() { if v := recover(); v != nil { done <- &propagatedPanic{ val: v, stack: debug.Stack(), } } else { done <- nil } }() doSomethingThatMightPanic() }() if val := <-done; val != nil { panic(val) } } // conc func main() { var wg conc.WaitGroup wg.Go(doSomethingThatMightPanic) // panics with a nice stacktrace wg.Wait() } 安装 使用以下命令进行安装：go get github.com/sourcegraph/conc
...

 [post link to conc 一个更好的 go 并发库](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/) [Go to Top (Alt + G)](https://jasminides.com/tags/conc/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fconc%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801958267&bpp=3&bdt=186&idt=164&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=1320691443348&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95344790%2C95355965&oid=2&pvsid=3470539782739464&tmod=1420602777&uas=0&nvt=1&fsapi=1&fc=1920&brdim=110%2C110%2C110%2C110%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=187)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Better Concurrency in Go
目录

- [前言](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/#%e5%89%8d%e8%a8%80)
- [安装](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/#%e5%ae%89%e8%a3%85)
- [介绍](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/#%e4%bb%8b%e7%bb%8d)
  - [conc.WaitGroup](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/#concwaitgroup)
  - [goroutine 池](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/#goroutine-%e6%b1%a0)
  - [Stream](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/#stream)
- [小结](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/#%e5%8f%82%e8%80%83)

## 前言

本文介绍 conc - 一个更好的 go 并发库，sourcegraph 在日常开发中使用 go 原生并发出现了问题，由此开发了 conc，相比标准并发代码更优雅，代码更少，下面展示一个例子，可以看出代码减少了许多。

```go
type propagatedPanic struct {
    val   any
    stack []byte
}

func main() {
    done := make(chan *propagatedPanic)
    go func() {
        defer func() {
            if v := recover(); v != nil {
                done <- &propagatedPanic{
                    val:   v,
                    stack: debug.Stack(),
                }
            } else {
                done <- nil
            }
        }()
        doSomethingThatMightPanic()
    }()
    if val := <-done; val != nil {
        panic(val)
    }
}

// conc

func main() {
    var wg conc.WaitGroup
    wg.Go(doSomethingThatMightPanic)
    // panics with a nice stacktrace
    wg.Wait()
}

```

复制

## 安装

使用以下命令进行安装： `go get github.com/sourcegraph/conc`

接下来对 conc 如何使用进行介绍。

## 介绍

### conc.WaitGroup

conc.WaitGroup 与标准库 sync.WaitGroup 的区别在于 conc.WaitGroup 中子 goroutine 中的 panic 会被传递给 Wait 方法的调用方，避免去 recover goroutine 的 panic.

例子：

```go
func main() {
	var count atomic.Int64

	var wg conc.WaitGroup
	for i := 1; i < 100; i++ {
		wg.Go(func() {
			count.Add(1)
		})
	}
	wg.Wait()

	fmt.Println(count.Load())
}

```

复制

如果想要 recover 某个 goroutine 发生的 panic，可以使用 WaitAndRecover 方法：

```go
func main() {
	var count atomic.Int64

	var wg conc.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Go(func() {
			if i == 7 {
				panic("bad thing")
			}
			count.Add(1)
		})
	}
	wg.WaitAndRecover()

	fmt.Println(count.Load())
}

```

复制

### goroutine 池

Pool 是用于处理并发任务的 goroutine 池，Pool 中的 goroutine 是延迟启动的，所以创建一个新的 Pool 是廉价的。产生的 goroutine 永远不会多于提交的任务。池是高效的，但不是零成本。它不应该用于非常短的任务。启动和拆卸的开销约为 1μs，每个任务的开销约为 300ns。

例子：

```go
func main() {
	p := pool.New().WithMaxGoroutines(3)
	for i := 0; i < 5; i++ {
		p.Go(func() {
			fmt.Println("conc")
		})
	}
	p.Wait()
}

```

复制

使用 WithContext 可以创建一个传递 Context 的 Pool，通过这个父 Context 来控制池中的 goroutine。默认情况下，在取消父 Context 之前，Pool 中的 Context 不会取消。如果需要在出现 panic 或错误时取消 context 可以通过配置
WithCancelOnError 来实现，例子：

```go
func main() {
	p := pool.New().
		WithMaxGoroutines(4).
		WithContext(context.Background()).
		WithCancelOnError()
	for i := 0; i < 3; i++ {
		i := i
		p.Go(func(ctx context.Context) error {
			if i == 2 {
				return errors.New("I will cancel all other tasks!")
			}
			<-ctx.Done()
			return nil
		})
	}
	err := p.Wait()
	fmt.Println(err)
}

```

复制

ResultPool 是一个执行返回泛型结果的任务池。使用 Go() 在池中执行任务，然后由 Wait() 返回任务的结果。例子：

```go
p := pool.NewWithResults[int]()
	for i := 0; i < 10; i++ {
		i := i
		p.Go(func() int {
			return i * 2
		})
	}
	res := p.Wait()
	// Result order is nondeterministic, so sort them first
	sort.Ints(res)
	fmt.Println(res)

```

复制

### Stream

Pool 执行任务返回的顺序是无序的，想要有序的结果可以使用 Stream。要使用 Stream，您需要提交一定数量的 Task，每个任务都会返回一个回调。每个任务都将在任务池中同时执行，并且回调将按照任务提交的顺序顺序执行。
任务提交完需使用 Wait() 方法等待任务执行完并传递 panic.

同 Pool 一样，Stream 也不适用于非常短的任务。启动和拆卸会增加几微秒的开销，每个任务的开销大约是 500ns。

例子：

```go
func main() {
	times := []int{20, 52, 16, 45, 4, 80}

	stream := stream2.New()
	for _, millis := range times {
		dur := time.Duration(millis) * time.Millisecond
		stream.Go(func() stream2.Callback {
			time.Sleep(dur)
			// This will print in the order the tasks were submitted
			return func() { fmt.Println(dur) }
		})
	}
	stream.Wait()
}

```

复制

## 小结

conc 相较于标准库的并发处理库，代码更加简洁，使用更加方便，是一套非常适合初学者的并发工具。

## 参考

- [https://about.sourcegraph.com/blog/building-conc-better-structured-concurrency-for-go](https://about.sourcegraph.com/blog/building-conc-better-structured-concurrency-for-go)
- [https://github.com/sourcegraph/conc](https://github.com/sourcegraph/conc)
- [https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/)

[Go to Top (Alt + G)](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/#top "Go to Top (Alt + G)")

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

## Better Go Concurrency
前言 本文介绍 conc - 一个更好的 go 并发库，sourcegraph 在日常开发中使用 go 原生并发出现了问题，由此开发了 conc，相比标准并发代码更优雅，代码更少，下面展示一个例子，可以看出代码减少了许多。
type propagatedPanic struct { val any stack \[\]byte } func main() { done := make(chan \*propagatedPanic) go func() { defer func() { if v := recover(); v != nil { done <- &propagatedPanic{ val: v, stack: debug.Stack(), } } else { done <- nil } }() doSomethingThatMightPanic() }() if val := <-done; val != nil { panic(val) } } // conc func main() { var wg conc.WaitGroup wg.Go(doSomethingThatMightPanic) // panics with a nice stacktrace wg.Wait() } 安装 使用以下命令进行安装：go get github.com/sourcegraph/conc
...

 [post link to conc 一个更好的 go 并发库](https://jasminides.com/posts/conc-better_structured_concurrency_for_go/) [Go to Top (Alt + G)](https://jasminides.com/tags/concurrency/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fconcurrency%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801978983&bpp=9&bdt=141&idt=208&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=4977842854776&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95344788%2C95353451%2C95355965%2C95340253%2C95340255&oid=2&pvsid=1186402978207610&tmod=483555977&uas=0&nvt=1&fsapi=1&fc=1920&brdim=120%2C120%2C120%2C120%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=236)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## Kubernetes Traffic Policy
目录

- [前言](https://jasminides.com/posts/kubernetes_externaltrafficpolicy/#%e5%89%8d%e8%a8%80)
- [简介](https://jasminides.com/posts/kubernetes_externaltrafficpolicy/#%e7%ae%80%e4%bb%8b)
- [区别](https://jasminides.com/posts/kubernetes_externaltrafficpolicy/#%e5%8c%ba%e5%88%ab)
  - [Cluster 模式](https://jasminides.com/posts/kubernetes_externaltrafficpolicy/#cluster-%e6%a8%a1%e5%bc%8f)
  - [Local 模式](https://jasminides.com/posts/kubernetes_externaltrafficpolicy/#local-%e6%a8%a1%e5%bc%8f)
- [参考](https://jasminides.com/posts/kubernetes_externaltrafficpolicy/#%e5%8f%82%e8%80%83)

## 前言

最近在使用 Kubernetes 查看 pod 日志时，发现 pod 日志显示的 ip 不是真实的请求者 ip, 而是 Node 节点的 ip。通过查阅资料发现可以通过设置 externalTrafficPolicy 来显示真实的 IP。

本文对 externaltrafficpolicy 进行一个简单的介绍。

## 简介

ExternalTrafficPolicy 是 Kubernetes Service 对象的一个属性，它决定了流量如何从集群外部访问 Service。有两个可选值：Cluster 和 Local。

Cluster 模式：
在 Cluster 模式下，流量将通过负载均衡器分发到 Service 的所有 Pod 上。这是传统的负载均衡方式，适用于需要水平扩展和容错的场景。负载均衡器会将流量平均分配给所有可用的 Pod，从而实现负载均衡。

Local 模式：
在 Local 模式下，流量将直接访问与请求最近的节点上运行的 Pod。这种方式避免了负载均衡器的介入，直接将流量定向到本地的 Pod 上。这样可以减少延迟，并且在负载均衡器发生故障时仍然保持可用性。

## 区别

两种模式有什么区别呢？

### Cluster 模式

Cluster 模式是默认的模式，Kube-proxy 不管容器在哪个节点上，会公平的转发到某一个节点上，在转发时会替换掉源 ip，变成转发的上一个节点的 ip.原因是 Kube-proxy 在做转发的时候，会做一次 SNAT (source network address translation)，所以源 ip 变成了上一个节点的 ip 地址。

这个模式的优点是负载均衡比较好，缺点是由于转发，可能会有性能损耗。

### Local 模式

Local 模式下，请求只转发给本机的容器，不会转发给其它节点的容器，保留了源 ip。

这个模式的优缺点跟 Cluster 模式恰恰相反：性能好，负载均衡不好。所以如果想要负载均衡就需要一层 LB 来进行控制。

## 参考

- [https://github.com/apache/apisix-ingress-controller/issues/1166](https://github.com/apache/apisix-ingress-controller/issues/1166)
- [https://medium.com/pablo-perez/k8s-externaltrafficpolicy-local-or-cluster-40b259a19404](https://medium.com/pablo-perez/k8s-externaltrafficpolicy-local-or-cluster-40b259a19404)
- [https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/)

[Go to Top (Alt + G)](https://jasminides.com/posts/kubernetes_externaltrafficpolicy/#top "Go to Top (Alt + G)")

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

## Clarity Tool Overview
前言 最近发现了一个新的工具-clarity, clarity 是一种免费工具，用于捕获用户使用网站。安装非常简单，可以在数分钟内开始获取数据。
clarity 有以下功能特点：
热点地图：为你的所有页面自动生成。查看用户点击的位置、他们忽略的内容以及滚动的距离。 insights: 快速发现用户在何处感到灰心，并将这些问题转化为机会。 Google Analytics: 可以方便的与 Google Analytics 关联。 会话录制：观看用户如何使用你的网站。了解运行顺畅的地方、需要改进的内容，并测试新想法。 copilot: 使用由 GPT 构建的直观对话体验来理解你的分析数据。 接下来就开始介绍 clarity 的简单使用。
clarity 使用 创建项目 登录成功后，可以选择网站或者移动项目，这里选择网站，输入相应的信息。
配置代码 填完信息，需要配置相应的代码信息，可以看到有 2 种方法，一种是知名第三方平台提供的快捷配置方法另一种是手动添加代码。这里选择手动添加代码。
配置信息 根据导览，可以配置一些信息，例如与 ga 关联，屏蔽一些隐私信息。
查看数据 根据导览的指引配置完信息后，第二天再次登录系统就可以看到数据了。可以看到有 4 个主要的模块栏目：仪表盘、录制、热度地图、ga，接下来分别介绍这 4 个部分。
仪表盘 仪表盘主要就是用户在你网站上访问的整体数据的展现。
录制 录制通过名字就可以得知这个是对用户在你页面上浏览情况的录制，可以看到用户的访问的整体情况，点击了哪些元素等。
热度地图 热度地图可以看到网站的哪些页面经常被访问，被访问的页面哪些部分经常被点击。
Google Analytics Google Analytics 主要就是 ga 的数据了。
...

 [post link to clarity 学习](https://jasminides.com/posts/clarity_learn/) [Go to Top (Alt + G)](https://jasminides.com/tags/clarity/#top "Go to Top (Alt + G)")

## Clarity Usage Guide
目录

- [前言](https://jasminides.com/posts/clarity_learn/#%e5%89%8d%e8%a8%80)
- [clarity 使用](https://jasminides.com/posts/clarity_learn/#clarity-%e4%bd%bf%e7%94%a8)
  - [创建项目](https://jasminides.com/posts/clarity_learn/#%e5%88%9b%e5%bb%ba%e9%a1%b9%e7%9b%ae)
  - [配置代码](https://jasminides.com/posts/clarity_learn/#%e9%85%8d%e7%bd%ae%e4%bb%a3%e7%a0%81)
  - [配置信息](https://jasminides.com/posts/clarity_learn/#%e9%85%8d%e7%bd%ae%e4%bf%a1%e6%81%af)
  - [查看数据](https://jasminides.com/posts/clarity_learn/#%e6%9f%a5%e7%9c%8b%e6%95%b0%e6%8d%ae)
  - [仪表盘](https://jasminides.com/posts/clarity_learn/#%e4%bb%aa%e8%a1%a8%e7%9b%98)
  - [录制](https://jasminides.com/posts/clarity_learn/#%e5%bd%95%e5%88%b6)
  - [热度地图](https://jasminides.com/posts/clarity_learn/#%e7%83%ad%e5%ba%a6%e5%9c%b0%e5%9b%be)
  - [Google Analytics](https://jasminides.com/posts/clarity_learn/#google-analytics)
- [小结](https://jasminides.com/posts/clarity_learn/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/clarity_learn/#%e5%8f%82%e8%80%83)

## 前言

最近发现了一个新的工具-clarity, clarity 是一种免费工具，用于捕获用户使用网站。安装非常简单，可以在数分钟内开始获取数据。

clarity 有以下功能特点：

- 热点地图：为你的所有页面自动生成。查看用户点击的位置、他们忽略的内容以及滚动的距离。
- insights: 快速发现用户在何处感到灰心，并将这些问题转化为机会。
- Google Analytics: 可以方便的与 Google Analytics 关联。
- 会话录制：观看用户如何使用你的网站。了解运行顺畅的地方、需要改进的内容，并测试新想法。
- copilot: 使用由 GPT 构建的直观对话体验来理解你的分析数据。

接下来就开始介绍 clarity 的简单使用。

## clarity 使用

### 创建项目

登录成功后，可以选择网站或者移动项目，这里选择网站，输入相应的信息。

![img.png](https://jasminides.com/img/clarity/img.png)

### 配置代码

填完信息，需要配置相应的代码信息，可以看到有 2 种方法，一种是知名第三方平台提供的快捷配置方法另一种是手动添加代码。这里选择手动添加代码。

![img_1.png](https://jasminides.com/img/clarity/img_1.png)

![img_2.png](https://jasminides.com/img/clarity/img_2.png)

### 配置信息

根据导览，可以配置一些信息，例如与 ga 关联，屏蔽一些隐私信息。

![img_3.png](https://jasminides.com/img/clarity/img_3.png)

![img_4.png](https://jasminides.com/img/clarity/img_4.png)

### 查看数据

根据导览的指引配置完信息后，第二天再次登录系统就可以看到数据了。可以看到有 4 个主要的模块栏目：仪表盘、录制、热度地图、ga，接下来分别介绍这 4 个部分。

![img_5.png](https://jasminides.com/img/clarity/img_5.png)

### 仪表盘

仪表盘主要就是用户在你网站上访问的整体数据的展现。

### 录制

录制通过名字就可以得知这个是对用户在你页面上浏览情况的录制，可以看到用户的访问的整体情况，点击了哪些元素等。

![img_6.png](https://jasminides.com/img/clarity/img_6.png)

### 热度地图

热度地图可以看到网站的哪些页面经常被访问，被访问的页面哪些部分经常被点击。

![img_7.png](https://jasminides.com/img/clarity/img_7.png)

![img_8.png](https://jasminides.com/img/clarity/img_8.png)

### Google Analytics

Google Analytics 主要就是 ga 的数据了。

## 小结

本文简单的介绍了 clarity 的使用，由于目前数据量较少，不能很好的展示 clarity 的功能。

clarity 的代码已经开源了，有兴趣的可以访问 `https://github.com/microsoft/clarity?tab=readme-ov-file` 查看。

## 参考

- [https://clarity.microsoft.com/](https://clarity.microsoft.com/)
- [https://clarity.microsoft.com/demo/projects/view/3t0wlogvdz/dashboard](https://clarity.microsoft.com/demo/projects/view/3t0wlogvdz/dashboard)
- [https://www.capterra.com/p/236349/Microsoft-Clarity/](https://www.capterra.com/p/236349/Microsoft-Clarity/)
- [https://learn.microsoft.com/en-us/clarity/](https://learn.microsoft.com/en-us/clarity/)
- [https://github.com/microsoft/clarity](https://github.com/microsoft/clarity)
- [https://learn.microsoft.com/en-us/clarity/ga-integration/ga-integration#how-to-find-and-add-your-account-id-on-google-analytics](https://learn.microsoft.com/en-us/clarity/ga-integration/ga-integration#how-to-find-and-add-your-account-id-on-google-analytics)

[Go to Top (Alt + G)](https://jasminides.com/posts/clarity_learn/#top "Go to Top (Alt + G)")

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

## Clarity Tool Overview
前言 最近发现了一个新的工具-clarity, clarity 是一种免费工具，用于捕获用户使用网站。安装非常简单，可以在数分钟内开始获取数据。
clarity 有以下功能特点：
热点地图：为你的所有页面自动生成。查看用户点击的位置、他们忽略的内容以及滚动的距离。 insights: 快速发现用户在何处感到灰心，并将这些问题转化为机会。 Google Analytics: 可以方便的与 Google Analytics 关联。 会话录制：观看用户如何使用你的网站。了解运行顺畅的地方、需要改进的内容，并测试新想法。 copilot: 使用由 GPT 构建的直观对话体验来理解你的分析数据。 接下来就开始介绍 clarity 的简单使用。
clarity 使用 创建项目 登录成功后，可以选择网站或者移动项目，这里选择网站，输入相应的信息。
配置代码 填完信息，需要配置相应的代码信息，可以看到有 2 种方法，一种是知名第三方平台提供的快捷配置方法另一种是手动添加代码。这里选择手动添加代码。
配置信息 根据导览，可以配置一些信息，例如与 ga 关联，屏蔽一些隐私信息。
查看数据 根据导览的指引配置完信息后，第二天再次登录系统就可以看到数据了。可以看到有 4 个主要的模块栏目：仪表盘、录制、热度地图、ga，接下来分别介绍这 4 个部分。
仪表盘 仪表盘主要就是用户在你网站上访问的整体数据的展现。
录制 录制通过名字就可以得知这个是对用户在你页面上浏览情况的录制，可以看到用户的访问的整体情况，点击了哪些元素等。
热度地图 热度地图可以看到网站的哪些页面经常被访问，被访问的页面哪些部分经常被点击。
Google Analytics Google Analytics 主要就是 ga 的数据了。
...

 [post link to clarity 学习](https://jasminides.com/posts/clarity_learn/) [Go to Top (Alt + G)](https://jasminides.com/tags/microsoft/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fmicrosoft%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801979114&bpp=6&bdt=236&idt=85&shv=r20250319&mjsv=m202503200101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=6445703821405&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C31091181%2C31091179%2C95355300&oid=2&pvsid=694068977254827&tmod=68774774&uas=0&nvt=1&fsapi=1&fc=1920&brdim=230%2C230%2C230%2C230%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=105)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## PostgreSQL CTE Guide
前言 本文介绍如何使用 CTE 表达式来简化 PostgreSQL 中的一些复杂查询。那 CTE 表达式是什么呢？
CTE 介绍 在 PostgreSql 中 WITH 提供了一种方式来书写在一个大型查询中使用的辅助语句。这些语句通常被称为公共表表达式或 CTE（Common Table Expressions），它们可以被看成是定义只在一个查询中存在的临时表。在 WITH 子句中的每一个辅助语句可以是一个 SELECT、INSERT、UPDATE 或 DELETE，并且 WITH 子句本身也可以被附加到一个主语句，主语句也可以是 SELECT、INSERT、UPDATE 或 DELETE。在 PostgreSQL 中，WITH 子句提供了一种编写辅助语句的方法，以便在复杂的查询中使用。
使用 该如何创建 CTE 呢，创建 CTE 的语句如下：
WITH cte\_name AS ( SELECT column1, column2, ... FROM table\_name WHERE condition ... ) SELECT \* FROM cte\_name; 在日常查询中 CTE 用于哪些场景呢：
递归查询：CTE 表达式常用于执行递归查询。通过在 CTE 表达式中引用自身，可以简洁地实现递归操作。 复杂查询：CTE 表达式可以用于构建复杂的查询，将查询逻辑分解为更易于理解和维护的部分。每个 CTE 子查询块可以负责不同的逻辑操作，最终组合成一个完整的查询。 数据转换和重组：CTE 表达式可以用于对数据进行转换和重组。通过在不同的 CTE 子查询块中选择、过滤和连接数据，可以生成新的结果集。 递归查询 WITH 表达式如何实现递归查询呢，可以通过添加 RECURSIVE 修饰符来实现。下面是一个示例：
...

 [post link to Postgresql CTE 表达式](https://jasminides.com/posts/postgresql_cte_expressions/) [Go to Top (Alt + G)](https://jasminides.com/tags/cte/#top "Go to Top (Alt + G)")

[iframe](https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2240998016636586&output=html&adk=3046330955&adf=2044148826&abgtt=6&lmt=1742201735&plat=3%3A16%2C4%3A16%2C9%3A32768%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&format=0x0&url=https%3A%2F%2Fjasminides.com%2Ftags%2Fcte%2F&pra=5&wgl=1&aihb=0&asro=0&ailel=1~2~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aiael=1~2~3~4~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&aicel=33~38&aifxl=29_18~30_19&aiixl=29_5~30_6&aiapm=0.15&aiapmi=0.33938&aiact=0.5&ailct=0.6&uach=WyJMaW51eCB4ODZfNjQiLCI2LjYuNzIiLCJ4ODYiLCIiLCIxMzQuMC42OTk4LjExNyIsbnVsbCwwLG51bGwsIjY0IixbWyJDaHJvbWl1bSIsIjEzNC4wLjY5OTguMTE3Il0sWyJOb3Q6QS1CcmFuZCIsIjI0LjAuMC4wIl0sWyJHb29nbGUgQ2hyb21lIiwiMTM0LjAuNjk5OC4xMTciXV0sMF0.&dt=1742801979191&bpp=2&bdt=186&idt=61&shv=r20250319&mjsv=m202503180101&ptt=9&saldr=aa&abxe=1&cookie_enabled=1&eoidce=1&nras=1&correlator=5898562970820&frm=20&pv=2&u_tz=-540&u_his=2&u_h=1024&u_w=1280&u_ah=1024&u_aw=1280&u_cd=24&u_sd=1&dmc=8&adx=-12245933&ady=-12245933&biw=1920&bih=100000&scr_x=0&scr_y=0&eid=95355340%2C95340252%2C95340254&oid=2&pvsid=2889726087086209&tmod=936753781&uas=0&nvt=1&fsapi=1&fc=1920&brdim=220%2C220%2C220%2C220%2C1280%2C0%2C1920%2C1080%2C1920%2C100000&vis=1&rsz=%7C%7Cs%7C&abl=NS&fu=32768&bc=31&bz=1&td=1&tdf=2&psd=W251bGwsbnVsbCxudWxsLDNd&nt=1&ifi=1&uci=a!1&fsb=1&dtd=77)

[iframe](https://googleads.g.doubleclick.net/pagead/html/r20250319/r20190131/zrt_lookup_fy2021.html)

## PostgreSQL CTE and JSON
前言 本文介绍如何使用 CTE 表达式来简化 PostgreSQL 中的一些复杂查询。那 CTE 表达式是什么呢？
CTE 介绍 在 PostgreSql 中 WITH 提供了一种方式来书写在一个大型查询中使用的辅助语句。这些语句通常被称为公共表表达式或 CTE（Common Table Expressions），它们可以被看成是定义只在一个查询中存在的临时表。在 WITH 子句中的每一个辅助语句可以是一个 SELECT、INSERT、UPDATE 或 DELETE，并且 WITH 子句本身也可以被附加到一个主语句，主语句也可以是 SELECT、INSERT、UPDATE 或 DELETE。在 PostgreSQL 中，WITH 子句提供了一种编写辅助语句的方法，以便在复杂的查询中使用。
使用 该如何创建 CTE 呢，创建 CTE 的语句如下：
WITH cte\_name AS ( SELECT column1, column2, ... FROM table\_name WHERE condition ... ) SELECT \* FROM cte\_name; 在日常查询中 CTE 用于哪些场景呢：
递归查询：CTE 表达式常用于执行递归查询。通过在 CTE 表达式中引用自身，可以简洁地实现递归操作。 复杂查询：CTE 表达式可以用于构建复杂的查询，将查询逻辑分解为更易于理解和维护的部分。每个 CTE 子查询块可以负责不同的逻辑操作，最终组合成一个完整的查询。 数据转换和重组：CTE 表达式可以用于对数据进行转换和重组。通过在不同的 CTE 子查询块中选择、过滤和连接数据，可以生成新的结果集。 递归查询 WITH 表达式如何实现递归查询呢，可以通过添加 RECURSIVE 修饰符来实现。下面是一个示例：
...

 [post link to Postgresql CTE 表达式](https://jasminides.com/posts/postgresql_cte_expressions/)

问题 最近在使用 sql 进行数值计算时，发现 sql 语句运行报错，报错信息如下：division by zero，综合分析 sql 语句得出是在进行除法运算时，除数为 0 导致的。
解决 接下来我来介绍几种解决这种问题的方法：
NULLIF 和 COALESCE 函数 我们可以使用 NULLIF 函数检查变量是否是 0 值，如果是 0 则为 null。使用 COALESCE 函数检查分子和分母是否有 NULL 值，然后返回默认值。
例子：
SELECT COALESCE(dividend / NULLIF(divisor, 0), default\_value) FROM xx CASE 表达式 我们可以使用 case when 来检查除数是否为 0，如果是 0 则使用默认值。 例子：
SELECT COALESCE(dividend / NULLIF(divisor, 0), default\_value) FROM xx 最终我采用了第一种方法，顺利的解决了问题，还需要多说的是在 postgresql sql 语句使用过程中，要注意所使用函数需要的参数的类型，遇到需要转换参数类型的情况，可以使用 case 函数进行类型转换。
小结 本文讲述了我遇到的 PostgreSQL 进行数值计算时遇到的 division by zero 问题的情况及解决方法。
参考 https://www.postgresql.org/docs/current/functions-conditional.html#FUNCTIONS-NULLIF https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-EXPRESS-EVAL https://pganalyze.com/docs/log-insights/app-errors/U128 https://stackoverflow.com/questions/17681375/avoid-division-by-zero-in-postgresql

 [post link to PostgreSQL 怎么解决 division by zero 问题](https://jasminides.com/posts/postgresql%E6%80%8E%E4%B9%88%E8%A7%A3%E5%86%B3division_by_zero%E9%97%AE%E9%A2%98/)

最近工作需要使用 sql 语句进行 Postgresql json 类型字段的查询，本文特此记录下一些常用的函数。
Postgresql json 类型简介 postgresql 支持两种 json 数据类型：json 和 jsonb，而两者唯一的区别在于效率，json 是对输入的完整拷贝，使用时再去解析，所以它会保留输入的空格，重复键以及顺序等。而 jsonb 是解析输入后保存的二进制，它在解析时会删除不必要的空格和重复的键，顺序和输入可能也不相同。使用时不用再次解析。两者对重复键的处理都是保留最后一个键值对。效率的差别：json 类型存储快，使用慢，jsonb 类型存储稍慢，使用较快。
json 类型操作符 我们先介绍 json 和 jsonb 的一些常用通用操作符：
操作符 右操作数类型 描述 示例 结果 -\> int 获取 JSON 数组元素（索引从 0 开始） select ‘\[{“a”:“foo”},{“b”:“bar”},{“c”:“baz”}\]’::json->2; {“c”:“baz”} -> text 通过键获取值 select ‘{“a”: {“b”:“foo”}}’::json->‘a’; {“b”:“foo”} -» int 获取 JSON 数组元素为 text select ‘\[1,2,3\]’::json-»2; 3 -» text 通过键获取值为 text select ‘{“a”:1,“b”:2}’::json-»‘b’; 2 jsonb 独有的操作符 操作符 右操作数类型 描述 示例 结果 @> jsonb 左侧 json 最上层的值是否包含右边 json 对象 select ‘{“a”:{“b”:2}}’::jsonb @> ‘{“b”:2}’::jsonb;
select ‘{“a”:1, “b”:2}’::jsonb @> ‘{“b”:2}’::jsonb; f
t <@ jsonb 左侧 json 对象是否包含于右侧 json 最上层的值内 select ‘{“b”:2}’::jsonb <@ ‘{“a”:1, “b”:2}’::jsonb; t ? text text 是否作为左侧 Json 对象最上层的键 select ‘{“a”:1, “b”:2}’::jsonb ? ‘b’; t ?\| text\[\] text\[\]中的任一元素是否作为左侧 Json 对象最上层的键 select ‘{“a”:1, “b”:2, “c”:3}’::jsonb ?\| array\[‘b’, ‘c’\]; t ?& text\[\] text\[\]中的所有元素是否作为左侧 Json 对象最上层的键 select ‘\[“a”, “b”\]’::jsonb ?& array\[‘a’, ‘b’\]; t \|\| jsonb 连接两个 json 对象，组成一个新的 json 对象 select ‘\[“a”, “b”\]’::jsonb \|\| ‘\[“c”, “d”\]’::jsonb; \[“a”, “b”, “c”, “d”\] - text 删除左侧 json 对象中键为 text 的键值对 select ‘{“a”: “b”}’::jsonb - ‘a’; {} - integer 删除数组指定索引处的元素，如果索引值为负数，则从右边计算索引值。如果最上层容器内不是数组，则抛出错误。 select ‘\[“a”, “b”\]’::jsonb - 1; \[“a”\] 创建 json 类型 那我们该如何创建 json 类型呢，下面介绍一些常见的函数
...

 [post link to Postgresql 的 json 类型](https://jasminides.com/posts/postgresql%E7%9A%84json%E7%B1%BB%E5%9E%8B/)

本文我来讲解如何使用 APISIX 来代理 PostgreSQL 数据库服务。
初试 最开始我以为很简单，我采用了直接在 APISIX DashBoard 上配置了一条路由，配置好后，连接发现无法成功连接，提示连接失败。
经过仔细的思考，发现 PostgreSQL 是使用 TCP 协议的数据库，不能通过简单的 route 进行配置，必须使用 stream-proxy 进行代理，接下来我们来看看怎么样来进行配置。
stream-proxy TCP 是许多流行应用程序和服务的协议，例如 LDAP、MySQL 和 RTMP。UDP（用户数据报协议）是许多流行的非事务性应用程序的协议，例如 DNS、系统日志和 RADIUS。
APISIX 可以动态负载平衡 TCP/UDP 代理。在 Nginx 的世界里，我们把 TCP/UDP proxy 称为 stream proxy，APISIX 就遵循了这个说法。
启用 stream-proxy 要开启 APISIX 流代理需要在 APISIX 配置中开启，APISIX 默认是关闭的。
apisix: stream\_proxy: # TCP/UDP proxy tcp: # TCP proxy address list - 9100 - "127.0.0.1:9101" udp: # UDP proxy address list - 9200 - "127.0.0.1:9211" 如果 apisix.enable\_admin 为 true，则 HTTP 和流代理都启用了上述配置。
...

 [post link to 使用 APISIX 代理 PostgreSQL 数据库](https://jasminides.com/posts/%E4%BD%BF%E7%94%A8apisix%E4%BB%A3%E7%90%86postgresql%E6%9C%8D%E5%8A%A1/)

最近在使用 DataX 进行 PostgreSQL 和 PostgreSQL 之间的数据同步，在数据同步过程中，遇到了一个问题，在本文简单记录下问题和相应的解决方案。
问题 在一次数据同步中，DataX 执行失败，错误信息如下：
具体错误信息为：com.alibaba.datax.common.exception.DataXException: Code:\[DBUtilErrorCode-12\], Description:\[不支持的数据库类型. 请注意查看 DataX 已经支持的数据库类型以及数据库版本.\]. - 您的配 置文件中的列配置信息有误. 因为DataX 不支持数据库读取这种字段类型. 字段名:\[country\], 字段名称:\[1111\], 字段Java类型:\[java.lang.String\]. 请尝试使用数据库函数将其转换datax支持的类型 我的配置如下：
{ "job": { "setting": { "speed": { "channel": 3 }, "errorLimit": { "record": 0, "percentage": 0.02 } }, "content": \[ { "reader": { "name": "postgresqlreader", "parameter": { "username": "xasdas", "password": "xxx", "column": \[ "id", "country" \], "connection": \[ { "table": \[ "xx" \], "jdbcUrl": \[ "jdbc:postgresql://xxx:5432/xxxx" \] } \] } }, "writer": { "name": "postgresqlwriter", "parameter": { "username": "xxxx", "password": "x", "column": \[ "id", "country" \], "preSql": \[ \], "postSql": \[ \], "connection": \[ { "jdbcUrl": "jdbc:postgresql://xxx:5432/xxxx", "table": \[ "xx" \] } \] } } } \] } } 通过检查数据库字段，发现 country 字段是 jsonb 类型，DataX 不支持此类型，DataX 的支持列表：
...

 [post link to DataX 数据同步中遇到的问题](https://jasminides.com/posts/datax%E6%95%B0%E6%8D%AE%E5%90%8C%E6%AD%A5%E4%B8%AD%E9%81%87%E5%88%B0%E7%9A%84%E9%97%AE%E9%A2%98/)

问题 在我日常使用 PostgreSQL 数据库过程中，会遇到一个问题：我在重新创建一个数据库表时，往往会导入已有的数据，这样会导致新增表数据时，由于 id 采用了自增，会从 1 开始生成，然后由于已有数据的缘故，所以会导致 id 重复报错。
解决 查看了 stackoverflow 的一些回答，发现了一个解决方案：采用 ALTER SEQUENCE 语句进行修改。
ALTER SEQUENCE ALTER SEQUENCE — 更改序列生成器的定义
语法：
ALTER SEQUENCE \[ IF EXISTS \] name \[ AS data\_type \] \[ INCREMENT \[ BY \] increment \] \[ MINVALUE minvalue \| NO MINVALUE \] \[ MAXVALUE maxvalue \| NO MAXVALUE \] \[ START \[ WITH \] start \] \[ RESTART \[ \[ WITH \] restart \] \] \[ CACHE cache \] \[ \[ NO \] CYCLE \] \[ OWNED BY { table\_name.column\_name \| NONE } \] ALTER SEQUENCE \[ IF EXISTS \] name OWNER TO { new\_owner \| CURRENT\_ROLE \| CURRENT\_USER \| SESSION\_USER } ALTER SEQUENCE \[ IF EXISTS \] name RENAME TO new\_name ALTER SEQUENCE \[ IF EXISTS \] name SET SCHEMA new\_schema 参数：
...

 [post link to Postgresql 修改序列产生器](https://jasminides.com/posts/postgresql%E4%BF%AE%E6%94%B9%E5%BA%8F%E5%88%97%E4%BA%A7%E7%94%9F%E5%99%A8%E7%9A%84%E5%8F%82%E6%95%B0/) [Go to Top (Alt + G)](https://jasminides.com/tags/postgresql/#top "Go to Top (Alt + G)")

## PostgreSQL CTE Guide
目录

- [前言](https://jasminides.com/posts/postgresql_cte_expressions/#%e5%89%8d%e8%a8%80)
  - [CTE 介绍](https://jasminides.com/posts/postgresql_cte_expressions/#cte-%e4%bb%8b%e7%bb%8d)
- [使用](https://jasminides.com/posts/postgresql_cte_expressions/#%e4%bd%bf%e7%94%a8)
  - [递归查询](https://jasminides.com/posts/postgresql_cte_expressions/#%e9%80%92%e5%bd%92%e6%9f%a5%e8%af%a2)
- [小结](https://jasminides.com/posts/postgresql_cte_expressions/#%e5%b0%8f%e7%bb%93)
- [参考](https://jasminides.com/posts/postgresql_cte_expressions/#%e5%8f%82%e8%80%83)

## 前言

本文介绍如何使用 CTE 表达式来简化 PostgreSQL 中的一些复杂查询。那 CTE 表达式是什么呢？

### CTE 介绍

在 PostgreSql 中 WITH 提供了一种方式来书写在一个大型查询中使用的辅助语句。这些语句通常被称为公共表表达式或 CTE（Common Table Expressions），它们可以被看成是定义只在一个查询中存在的临时表。在 WITH 子句中的每一个辅助语句可以是一个 SELECT、INSERT、UPDATE 或 DELETE，并且 WITH 子句本身也可以被附加到一个主语句，主语句也可以是 SELECT、INSERT、UPDATE 或 DELETE。在 PostgreSQL 中，WITH 子句提供了一种编写辅助语句的方法，以便在复杂的查询中使用。

## 使用

该如何创建 CTE 呢，创建 CTE 的语句如下：

```sql
WITH cte_name AS (
    SELECT column1, column2, ...
    FROM table_name
WHERE condition
    ...
    )
SELECT *
FROM cte_name;

```

复制

在日常查询中 CTE 用于哪些场景呢：

- 递归查询：CTE 表达式常用于执行递归查询。通过在 CTE 表达式中引用自身，可以简洁地实现递归操作。
- 复杂查询：CTE 表达式可以用于构建复杂的查询，将查询逻辑分解为更易于理解和维护的部分。每个 CTE 子查询块可以负责不同的逻辑操作，最终组合成一个完整的查询。
- 数据转换和重组：CTE 表达式可以用于对数据进行转换和重组。通过在不同的 CTE 子查询块中选择、过滤和连接数据，可以生成新的结果集。

### 递归查询

WITH 表达式如何实现递归查询呢，可以通过添加 RECURSIVE 修饰符来实现。下面是一个示例：

```sql
WITH RECURSIVE t(n) AS (
    VALUES (1)
    UNION ALL
    SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;

```

复制

这个例子是对 1 到 100 之间数求和。

## 小结

PostgreSQL 的 CTE 表达式是一种强大的工具，可以帮助我们编写复杂且高效的查询语句。

## 参考

- [https://www.postgresql.org/docs/16/queries-with.html](https://www.postgresql.org/docs/16/queries-with.html)

[Go to Top (Alt + G)](https://jasminides.com/posts/postgresql_cte_expressions/#top "Go to Top (Alt + G)")

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

googleads.g.doubleclick.net

# googleads.g.doubleclick.net is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

## Go Strategy Pattern
目录

- [策略模式介绍](https://jasminides.com/posts/go_design-patterns_strategy/#%e7%ad%96%e7%95%a5%e6%a8%a1%e5%bc%8f%e4%bb%8b%e7%bb%8d)
  - [何时可以使用策略模式呢](https://jasminides.com/posts/go_design-patterns_strategy/#%e4%bd%95%e6%97%b6%e5%8f%af%e4%bb%a5%e4%bd%bf%e7%94%a8%e7%ad%96%e7%95%a5%e6%a8%a1%e5%bc%8f%e5%91%a2)
- [go 实现策略模式](https://jasminides.com/posts/go_design-patterns_strategy/#go-%e5%ae%9e%e7%8e%b0%e7%ad%96%e7%95%a5%e6%a8%a1%e5%bc%8f)
- [小结](https://jasminides.com/posts/go_design-patterns_strategy/#%e5%b0%8f%e7%bb%93)

今天介绍一个常见的设计模式 \- 策略模式，并基于一个简单的例子来讲解。

## 策略模式介绍

策略模式（Strategy Pattern）是一种行为型设计模式，它将一组算法封装成独立的对象，并使它们可以互相替换。这样做的好处是，可以在运行时动态地改变对象的行为，而不需要修改使用该对象的代码。

### 何时可以使用策略模式呢

我们在用 GO 编程的时候经常碰到多层控制语句，一层又一层，既不优雅，也不利于后续维护。比如下述这种：

```go
if xxx {
// do something
} else if xxx {
// do something
} else if xxx {
// do something
 else {
}

```

复制

虽然按这种模式写起来简单快捷，但它也违背了面向对象的两个原则：

- 单一职责原则：多个控制语句，意味着拥有多种功能；
- 开闭原则：当要进行修改时，原有代码不可避免要被修改；

此时就可以采用策略模式来替换这类多层控制语句。

## go 实现策略模式

go 语言该怎么实现策略模式呢？

在 Go 语言中，策略模式可以通过接口和函数来实现。首先，我们定义一个接口，该接口声明了算法执行的方法。然后，我们可以为每个具体的算法实现一个结构体，并实现接口中的方法。最后，我们可以在需要使用算法的地方，通过接口来调用具体的算法。

下面通过一个简单的例子来讲解策略模式，现在有这样一个场景我们现在有 2 个数据表，这 2 个数据表拥有相同的字段，都可以根据 name 来查询某个数据，我们需要根据参数的不同来决定使用哪种表进行查询，在没有使用策略模式时，我们往往使用大量的 if 来实现这个操作。
接下来由我来介绍策略模式来实现相同的操作。

先定义查询操作的接口：

```go
type DataStrategy interface {
	Query(name string)
}

```

复制

定义 2 张表的查询 struct，并实现 DataStrategy 接口：

```go

// table1 通过 table1 来查询
type table1 struct{}

func (s *table1) Query(name string) {
	fmt.Println("table1 query")
}

// table2
type table2 struct{}

func (s *table2) Query(name string) {
	fmt.Println("table2 query")
}

```

复制

再定义 Data 对象用来执行不同的策略：

```go
type Data struct {
	impl DataStrategy
}

func (r *Data) SetTable(i DataStrategy) {
	r.impl = i
}

func (r *Data) Query(name string) {
	r.impl.Query(name)
}

```

复制

运行代码：

```console
table1 query
table2 query

```

复制

## 小结

策略模式是一种非常有用的设计模式，它可以在不修改现有代码的情况下，动态地改变算法或行为。在 Go 语言中，我们可以通过接口和函数来实现策略模式。通过合理地应用策略模式，我们可以使代码更加灵活、可扩展，并提高代码的可维护性。

giscus

正在加载评论……

[Go to Top (Alt + G)](https://jasminides.com/posts/go_design-patterns_strategy/#top "Go to Top (Alt + G)")

