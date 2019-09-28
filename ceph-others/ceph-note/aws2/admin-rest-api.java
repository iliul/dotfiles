import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.*;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

import com.eclipsesource.json.Json;
import com.eclipsesource.json.JsonArray;
import com.eclipsesource.json.JsonObject;
import com.eclipsesource.json.JsonValue;
import org.apache.commons.codec.binary.Base64;


public class Main {
    static String accessKey = "admin";
    static String secretKey = "admin";
    static String cmd = "/admin/usage?format=json&uid=admin&show-entries=True&show-summary=True";
    static String resource = "/admin/usage";
    static String endPoint = "10.254.3.68:7480";

    public static void main(String[] args) throws Exception {
//************************获取用户列表***************************
        cmd = "/admin/metadata/user?format=json";
        resource = "/admin/metadata/user";
        String json_response = get();
        System.out.println("用户列表：" + json_response);
        JsonArray array = Json.parse(json_response).asArray();
        System.out.println("查询用户使用空间：");
        for (JsonValue value : array) {
            //**********从列表中获取某个用户
            System.out.println("用户：" + value.asString());
            cmd = "/admin/user?info&uid=" + value.asString() + "&stats=True";
            resource = "/admin/user";
            json_response = get();
            JsonObject object = Json.parse(json_response).asObject();

            //get()返回GET request not worked(自定义的我这里，404用户不存在，虽然在列表中有列出来，目前正在分析为何没有更新)
            if (object.get("stats").isString())
                System.out.println(object.get("stats").asString());
            //get()返回正常，用户存在，含有用户容量信息
            if (object.get("stats").isObject()) {
                System.out.println("用户容量信息：");
                System.out.println("num_kb:" + object.get("stats").asObject().get("num_kb"));
                System.out.println("num_kb_rounded:" + object.get("stats").asObject().get("num_kb_rounded"));
                System.out.println("num_objects:" + object.get("stats").asObject().get("num_objects"));
            }
        }
//*********************查询桶的数量
        System.out.println("查询用户桶数量：");
        for (JsonValue value : array) {
            //从列表中获取某个用户
            System.out.println("用户：" + value.asString());
            cmd = "/admin/bucket?info&uid=" + value.asString();
            resource = "/admin/bucket";
            json_response = get();
            JsonArray object = Json.parse(json_response).asArray();
            System.out.println("桶的数量为:" + object.size());
        }
    }
//http get request
    public static String get() {
        HttpURLConnection conn = null;
        try {
            URL url = new URL("http://" + endPoint + cmd);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            Date date = new Date();
            SimpleDateFormat dataformater = new SimpleDateFormat("EEE, d MMM yyyy HH:mm:ss z", Locale.ENGLISH);
            dataformater.setTimeZone(TimeZone.getTimeZone("GMT"));
            String dateString = dataformater.format(date);
            String sign = sign("GET", dateString, resource);
            conn.setRequestProperty("date", dateString);
            conn.setRequestProperty("Authorization", sign);
            conn.setRequestProperty("Host", endPoint);

            int responseCode = conn.getResponseCode();
            System.out.println("GET Response Code :: " + responseCode);
            if (responseCode == HttpURLConnection.HTTP_OK) { // success
                BufferedReader in = new BufferedReader(new InputStreamReader(
                        conn.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();
                return response.toString();
            } else {
                return "{\"stats\":\"404\"}";
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        } finally {

        }
    }
//************************aws2签名认证
    public static String sign(String httpVerb, String date, String resource) {
        String stringToSign = httpVerb
                + "\n\n\n"
                + date + "\n" + resource;
        try {
            Mac mac = Mac.getInstance("HmacSHA1");
            byte[] keyBytes = secretKey.getBytes("UTF8");
            SecretKeySpec signingKey = new SecretKeySpec(keyBytes, "HmacSHA1");
            mac.init(signingKey);
            byte[] signBytes = mac.doFinal(stringToSign.getBytes("UTF8"));
            Base64 encoder = new Base64();
            String signature = new String(encoder.encode(signBytes));
            return "AWS" + " " + accessKey + ":" + signature;
        } catch (Exception e) {
            throw new RuntimeException("MAC CALC FAILED.");
        }
    }
}
