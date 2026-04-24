# Benchmark Report — Lab #17 Multi-Memory Agent

## 1. Setup

- Number of conversations: 10
- Agent A: No-memory agent
- Agent B: With-memory agent
- Memory backends: short-term, profile, episodic, semantic
- LLM provider: openai
- Token budget: 1500

## 2. Results Summary

| # | Scenario | No-memory result | With-memory result | Pass? |
|---:|---|---|---|---|
| 1 | Recall user name after several turns | Xin lỗi, nhưng tôi không biết tên của bạn. Bạn có thể cho tôi biết tên của bạn không? | Tên bạn là Huy. | Pass |
| 2 | Preference recall | Dưới đây là một số framework backend đơn giản mà bạn có thể tham khảo:

1. **Flask** (Python): Flask là một micro-framework nhẹ và dễ sử dụng, rất phù hợp cho các dự án nhỏ và vừa. Nó cho phép bạn xây dựng ứng dụng web nhanh chóng với ít cấu hình.

2. **Express.js** (Node.js): Express là một framework web phổ biến cho Node.js, giúp bạn xây dựng ứng dụng và API một cách nhanh chóng và dễ dàng. Nó có nhiều middleware hỗ trợ.

3. **Django** (Python): Mặc dù Django là một framework lớn hơn, nhưng nó cũng có thể được sử dụng cho các dự án nhỏ nhờ vào tính năng "Django Admin" và các công cụ tích hợp sẵn.

4. **Ruby on Rails** (Ruby): Rails là một framework mạnh mẽ cho Ruby, giúp phát triển ứng dụng web nhanh chóng với nhiều tính năng tích hợp.

5. **Spring Boot** (Java): Spring Boot giúp đơn giản hóa việc phát triển ứng dụng Java, cho phép bạn tạo ra các ứng dụng độc lập và dễ triển khai.

6. **FastAPI** (Python): FastAPI là một framework hiện đại cho Python, rất nhanh và dễ sử dụng, đặc biệt cho việc xây dựng API.

Bạn có thể chọn framework phù hợp với ngôn ngữ lập trình mà bạn quen thuộc và yêu cầu của dự án của mình. | Một số framework backend đơn giản và phổ biến cho Python mà bạn có thể xem xét là:

1. **Flask**: Đây là một micro-framework rất nhẹ và dễ sử dụng. Flask cho phép bạn xây dựng ứng dụng web nhanh chóng với ít cấu hình hơn. Nó rất linh hoạt và có thể mở rộng dễ dàng.

2. **FastAPI**: Đây là một framework hiện đại cho việc xây dựng API với Python 3.6+ dựa trên tiêu chuẩn OpenAPI. FastAPI rất nhanh và hỗ trợ tự động tạo tài liệu API.

3. **Django**: Mặc dù Django là một framework lớn hơn, nó cung cấp nhiều tính năng tích hợp sẵn và có thể giúp bạn phát triển ứng dụng web một cách nhanh chóng. Nếu bạn cần một ứng dụng phức tạp hơn, Django có thể là lựa chọn tốt.

Nếu bạn cần thêm thông tin hoặc ví dụ cụ thể về cách sử dụng một trong các framework này, hãy cho tôi biết! | Pass |
| 3 | Allergy conflict update | Để đưa ra lời khuyên chính xác về thực phẩm cần tránh, tôi cần biết thêm thông tin về tình trạng sức khỏe, dị ứng hoặc mục tiêu dinh dưỡng của bạn. Tuy nhiên, dưới đây là một số loại thực phẩm mà nhiều người thường cần tránh hoặc hạn chế:

1. **Thực phẩm chế biến sẵn**: Chứa nhiều đường, muối và chất bảo quản.
2. **Đường tinh luyện**: Có thể gây tăng cân và các vấn đề sức khỏe khác.
3. **Chất béo bão hòa và chất béo trans**: Có trong thực phẩm chiên, đồ ăn nhanh và một số loại bánh kẹo.
4. **Thực phẩm chứa gluten**: Nếu bạn bị bệnh celiac hoặc nhạy cảm với gluten.
5. **Sữa và sản phẩm từ sữa**: Nếu bạn không dung nạp lactose hoặc có dị ứng với sữa.
6. **Thực phẩm giàu natri**: Như đồ ăn đóng hộp, có thể gây tăng huyết áp.

Nếu bạn có một tình trạng sức khỏe cụ thể hoặc mục tiêu dinh dưỡng, hãy cho tôi biết để tôi có thể cung cấp thông tin chi tiết hơn! | Nếu bạn dị ứng với đậu nành, bạn nên tránh tất cả các sản phẩm chứa đậu nành, bao gồm sữa đậu nành, đậu phụ, và các sản phẩm chế biến từ đậu nành khác. Ngoài ra, hãy kiểm tra nhãn sản phẩm để đảm bảo không có thành phần nào từ đậu nành. Nếu bạn cần thêm thông tin về cách quản lý dị ứng hoặc tìm kiếm sản phẩm thay thế, hãy cho tôi biết! | Pass |
| 4 | Episodic recall docker lesson | Để xác định nguyên nhân lỗi Docker của bạn, tôi cần thêm thông tin cụ thể về lỗi mà bạn đã gặp phải. Bạn có thể cung cấp thông báo lỗi hoặc mô tả tình huống khi lỗi xảy ra không? | Lỗi Docker của bạn lần trước là do bạn gọi localhost trong container. Khi bạn làm điều này, container không thể truy cập vào dịch vụ đang chạy trên máy chủ của bạn. Thay vào đó, bạn nên sử dụng địa chỉ IP của máy chủ hoặc tên mạng của dịch vụ trong Docker. | Pass |
| 5 | Semantic retrieval async and Celery | Background job và non-blocking request đều liên quan đến việc xử lý tác vụ mà không làm gián đoạn trải nghiệm người dùng, nhưng chúng có những điểm khác nhau cơ bản:

1. **Background Job**:
   - Là một tác vụ được thực hiện ở phía máy chủ mà không cần sự tương tác trực tiếp từ người dùng.
   - Thường được sử dụng cho các công việc tốn thời gian như xử lý dữ liệu, gửi email, hoặc thực hiện các tác vụ định kỳ.
   - Người dùng có thể không nhận được phản hồi ngay lập tức và thường không biết khi nào công việc sẽ hoàn thành. Kết quả có thể được thông báo sau đó qua email hoặc thông báo trong ứng dụng.

2. **Non-blocking Request**:
   - Là một yêu cầu mà không làm tắc nghẽn luồng chính của ứng dụng, cho phép người dùng tiếp tục tương tác với ứng dụng trong khi chờ đợi phản hồi từ máy chủ.
   - Thường được sử dụng trong các ứng dụng web để cải thiện trải nghiệm người dùng, ví dụ như khi tải dữ liệu từ máy chủ mà không làm mới trang.
   - Người dùng có thể thấy một thông báo tải hoặc một phần giao diện cập nhật khi dữ liệu được trả về.

Tóm lại, background job thường là các tác vụ chạy ở phía máy chủ mà không cần sự tương tác ngay lập tức từ người dùng, trong khi non-blocking request là cách thức gửi yêu cầu mà không làm gián đoạn trải nghiệm người dùng trong ứng dụng. | Vì bạn từng rối async/await và Celery: async/await giúp xử lý I/O không blocking trong request, còn Celery dùng cho background job chạy tách khỏi request lifecycle, có queue và retry. | Pass |
| 6 | Learning style profile | RabbitMQ là một hệ thống quản lý hàng đợi tin nhắn (message broker) mã nguồn mở, được viết bằng ngôn ngữ Erlang. Nó cho phép các ứng dụng giao tiếp với nhau thông qua việc gửi và nhận tin nhắn, giúp tách biệt các thành phần của ứng dụng và cải thiện khả năng mở rộng cũng như tính linh hoạt.

Dưới đây là một số điểm chính về RabbitMQ:

1. **Hàng đợi tin nhắn**: RabbitMQ sử dụng hàng đợi để lưu trữ tin nhắn cho đến khi chúng được xử lý. Điều này cho phép các ứng dụng gửi và nhận tin nhắn mà không cần phải kết nối trực tiếp với nhau.

2. **Mô hình xuất bản - đăng ký (Publish-Subscribe)**: RabbitMQ hỗ trợ mô hình này, cho phép một nhà xuất bản gửi tin nhắn đến nhiều người đăng ký cùng một lúc.

3. **Đảm bảo độ tin cậy**: RabbitMQ cung cấp các tính năng như xác nhận tin nhắn (message acknowledgment) và lưu trữ tin nhắn (message persistence) để đảm bảo rằng tin nhắn không bị mất trong quá trình truyền tải.

4. **Khả năng mở rộng**: RabbitMQ có thể được cấu hình để chạy trên nhiều máy chủ, cho phép mở rộng quy mô dễ dàng khi cần thiết.

5. **Hỗ trợ nhiều giao thức**: Mặc dù RabbitMQ chủ yếu sử dụng giao thức AMQP (Advanced Message Queuing Protocol), nó cũng hỗ trợ nhiều giao thức khác như MQTT và STOMP.

6. **Quản lý và giám sát**: RabbitMQ cung cấp giao diện quản lý web cho phép người dùng theo dõi và quản lý các hàng đợi, người tiêu dùng và các thông số khác.

RabbitMQ thường được sử dụng trong các ứng dụng phân tán, microservices, và các hệ thống cần xử lý tin nhắn theo cách không đồng bộ. | Tóm tắt ngắn: RabbitMQ là một hệ thống quản lý hàng đợi tin nhắn (message broker) mã nguồn mở, cho phép các ứng dụng giao tiếp với nhau thông qua việc gửi và nhận tin nhắn. | Pass |
| 7 | Current query overrides memory | Một số framework backend phổ biến trong Java mà bạn có thể sử dụng bao gồm:

1. **Spring Boot**: Đây là một trong những framework phổ biến nhất cho phát triển ứng dụng Java. Nó giúp bạn xây dựng ứng dụng nhanh chóng với cấu hình tối thiểu và hỗ trợ nhiều tính năng như RESTful API, bảo mật, và kết nối cơ sở dữ liệu.

2. **Java EE (Jakarta EE)**: Đây là một nền tảng tiêu chuẩn cho phát triển ứng dụng doanh nghiệp. Nó cung cấp nhiều API và công nghệ như Servlets, JSP, EJB, và JPA.

3. **Micronaut**: Là một framework hiện đại, nhẹ, được thiết kế cho microservices. Nó hỗ trợ lập trình phản ứng và có thời gian khởi động nhanh.

4. **Quarkus**: Được tối ưu hóa cho môi trường cloud và container, Quarkus hỗ trợ lập trình phản ứng và có khả năng khởi động nhanh, rất phù hợp cho các ứng dụng microservices.

5. **Dropwizard**: Là một framework nhẹ, kết hợp nhiều thư viện tốt nhất để xây dựng ứng dụng web nhanh chóng và hiệu quả.

Bạn có thể chọn một trong những framework này tùy thuộc vào yêu cầu và sở thích của dự án của bạn. | Nếu bạn phải sử dụng Java cho dự án backend của mình, có một số framework phổ biến mà bạn có thể xem xét:

1. **Spring Boot**: Đây là một trong những framework phổ biến nhất cho phát triển ứng dụng Java. Nó giúp bạn xây dựng các ứng dụng độc lập và dễ dàng triển khai. Spring Boot cung cấp nhiều tính năng như cấu hình tự động, tích hợp với cơ sở dữ liệu, và hỗ trợ RESTful API.

2. **Jakarta EE (trước đây là Java EE)**: Đây là một nền tảng mạnh mẽ cho phát triển ứng dụng doanh nghiệp. Jakarta EE cung cấp nhiều API và công nghệ cho phát triển ứng dụng web, dịch vụ web, và nhiều hơn nữa.

3. **Micronaut**: Đây là một framework hiện đại, nhẹ và nhanh, được thiết kế cho microservices. Micronaut hỗ trợ lập trình phản ứng và có khả năng khởi động nhanh.

4. **Quarkus**: Đây là một framework mới nổi, tối ưu hóa cho Kubernetes và cloud-native. Quarkus hỗ trợ lập trình phản ứng và có khả năng khởi động rất nhanh.

5. **Play Framework**: Đây là một framework cho phát triển ứng dụng web, hỗ trợ lập trình bất đồng bộ và có thể sử dụng với Scala hoặc Java.

Tùy thuộc vào yêu cầu cụ thể của dự án, bạn có thể chọn framework phù hợp nhất. Nếu bạn cần thêm thông tin về một framework cụ thể, hãy cho tôi biết! | Pass |
| 8 | Forget and delete memory | Xin lỗi, nhưng tôi không biết tên của bạn. Bạn có thể cho tôi biết tên của bạn không? | Xin lỗi, nhưng tôi không biết tên của bạn. Bạn có thể cho tôi biết tên của bạn không? | Pass |
| 9 | Trim context with important preference retention | Tôi không biết bạn thích ngôn ngữ nào, nhưng bạn có thể cho tôi biết về sở thích của bạn để tôi có thể giúp đỡ tốt hơn! | Bạn thích ngôn ngữ Python! Nếu bạn cần hỗ trợ hoặc có câu hỏi nào liên quan đến Python hoặc các dự án của bạn, hãy cho tôi biết nhé! | Pass |
| 10 | Semantic FAQ retrieval docker compose host | Trong container, để gọi đến database, bạn thường sử dụng tên của service hoặc container mà database đang chạy. Nếu bạn đang sử dụng Docker Compose, bạn có thể sử dụng tên service được định nghĩa trong file `docker-compose.yml` làm host.

Ví dụ, nếu bạn có một service database được định nghĩa như sau:

```yaml
services:
  db:
    image: postgres
```

Thì trong ứng dụng của bạn, bạn có thể kết nối đến database bằng cách sử dụng `db` làm host.

Nếu bạn không sử dụng Docker Compose, bạn có thể sử dụng địa chỉ IP của container database hoặc `localhost` nếu ứng dụng và database đang chạy trong cùng một container. Tuy nhiên, cách tốt nhất là sử dụng tên service để đảm bảo tính linh hoạt và dễ bảo trì. | Trong container, để gọi đến database, bạn thường sử dụng tên của service hoặc container mà database đang chạy. Nếu bạn đang sử dụng Docker Compose, bạn có thể sử dụng tên service được định nghĩa trong file `docker-compose.yml` làm host. Ví dụ, nếu bạn có một service database được gọi là `db`, bạn có thể kết nối đến database bằng cách sử dụng `db` làm host.

Nếu bạn không sử dụng Docker Compose, bạn có thể cần sử dụng địa chỉ IP của container hoặc tên máy chủ (hostname) của máy chủ mà container đang chạy. Hãy chắc chắn rằng các cổng cần thiết đã được mở và cấu hình đúng để cho phép kết nối từ container đến database. | Pass |

## 3. Metrics

| Metric | No-memory Agent | With-memory Agent | Notes |
|---|---:|---:|---|
| Memory hit rate (pass cases) | - | 10/10 | Rule-based evaluation from expected keywords |
| Conflict accuracy | thấp | cao hơn | Overwrite profile fact theo correction marker |
| Context utilization | thấp | cao hơn | Prompt có section memory + trim budget |

## 4. Privacy & Limitations

- Profile memory nhạy cảm nhất vì chứa fact trực tiếp về user.
- Episodic và semantic memory có rủi ro lộ lịch sử hành vi nếu sai user_id isolation.
- Deletion cần xóa đồng thời profile, episodic, semantic và short-term.
- TTL đề xuất: short-term theo session, episodic 30-90 ngày, profile theo consent.
- Limitations: router rule-based và semantic keyword fallback có thể sai với query mơ hồ.