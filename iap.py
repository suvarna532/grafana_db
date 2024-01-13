import jwt
from datetime import datetime, timedelta

def generate_iap_jwt(service_account_key_path, client_id, issuer):
    # Set the expiration time for the token (e.g., 1 hour from now)
    expiration_time = datetime.utcnow() + timedelta(hours=1)

    # Define the JWT claims
    claims = {
        "aud": client_id,
        "exp": expiration_time,
        "iat": datetime.utcnow(),
        "iss": issuer,
        "target_audience": "https://grafana.gc.vitalbook.com",
    }

    try:
        # Load the service account key
        #with open(service_account_key_path, "r") as key_file:
            #service_account_key = key_file.read()
        service_account_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC201DA/8RVuEur\nkWF2XgHn46vJ1OfJeAOkC3Z95z1i9VlWshVwIRzfzZz23vTxsrLE22xxjna5ZsU0\n+ebGArupeW9RXtWIUW5vMLbqxrLymI+rH9K+ESwyrzrMu/CLdvLBfLvmrQLGzOG/\nY/9FL+33lf/W3jbibCu4xRdlsMLhC6fKuerP+qnAxEqGUMxb1ayKVcU56tAiKujj\nbVIw0kQgCfATXNCNoq303rY4Jx+4sU10YGRfc12o1Jn/dOi6sQmIitq1JNuHsyAI\nkhj5mAYsLp2wTgzWnjzwVd4PgbTQ/sFkbnVPl3g5Wesm2NYGJKacsxIVCY0SUvn2\nvSRhWUN/AgMBAAECggEAAWeuS3herrDZiTUFYqsir9YQSC+9u+aJyV2Gche8Ht5w\nKHRGdX501iV36LD2zOVgioOHUrDmbAug5tVETGZDT5F/bqLIn6X0QvW2tpjrnVJw\nyT8L3Kfi3rdKNjmAyFAdiUqR+kl1m9+d+9i4WS10P11iUHwrxKjDmQflPY/Eb1Yw\nnwiqAJveX+zK41Md4lc/FywwwbVNMA4XBY3plvKXU0eCWUzvzTyRpZT6Y+rCEpmR\n1OF4B0YGhAB9myLKmlgj33Dw/AscKRadVjJXyJWV4LcIqS8ucnLzxGrLttCnXPR6\nRTZyp7ySkaWeeeZMTC1Q+Uf2ZarILgRtZ0UN96fD+QKBgQD60Y+kdefj5Anb9YVz\nBdsz3Q9iK8SeOUnqLo97hDBqjwcHsg/wlzZ5PhT4hxmeQudqVX158wQVrkRSN9e3\nuoKjztdJTStIwj6encUjq9d4EDedtCWScDraIL/Eeo2no5BVQLvHZQnRpkiZnKVF\n7RowqvbRipq9MzsSH9t/GtsfFwKBgQC6mi09gZtVMTxxRf0G8sbBNLuj+GxRF4df\n0gOJ+YJDUbp+6/AA1CaI/q95e7g9iMIlpbaZb1qAVo+mv0BJvAWfqrxD+Yr7ccRp\nSNn6Dnh46NUVNBpu70rLGIghZ28srITtRWXYCfOdaGXi7hBL4vGvVOmujFZcLVzl\nDBD5mfz/2QKBgQDi6RfEt450k2eAAV0btF6dSw6Rx/r3EekW3cyc9/g9TuwTQDo/\ndO2pPksGlGLO1MQ7ZOBBpWM6og/ZOgAEjc2GmKgX/qJ8Do9MPHuPS/WA/1rxZ3re\nQn5bvGkBPcZNtSHsnsXDHFuHuaHQpvC2lEyvXtwwse5P4Ls+KGgRU6CNPQKBgALt\nUDBazBj2AMC2HFXzkPKO5TKZPvm2qMT0AmIzq7tqmMZM5SLeMQyNEiuRqT4t2v3E\nL60Qdhb1RKOU9GkzrdLnVrSqQWfYTQBpyCGIAJPE8zK18oQy9LVi2R/NA41r11nx\ncLuGzG93p8F7gn3uPWRGrLO0N9aST5a4Lbv8kl9hAoGBAPeQepHuIKAUfaEOllOR\ngN0/Sjd3vc4eI25hpSr7/nFJDpsTzBUF2ZpbTMRc3Qt4t7cvjsgdvCPR50pKnsRK\n6yBdzJXrT+JAsP8HzSc3jAjktJmGqN3edXLakqystL3ZkM6ZOtZ87evpybIG6Uex\njptjeJWe/s9jEs8vEN0wabgz\n-----END PRIVATE KEY-----\n"

        # Sign the JWT token using the service account key
        jwt_token = jwt.encode(claims, service_account_key, algorithm="RS256")

        return jwt_token
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return None

# Replace 'path/to/your/service-account-key.json', 'your_client_id_here', and 'your_issuer_here' with your actual values
service_account_key_path = "service-account-key.json"
client_id = "102502383300749492869"
issuer = "vml-grafana@vst-main-logging.iam.gserviceaccount.com"

iap_jwt_token = generate_iap_jwt(service_account_key_path, client_id, issuer)
if iap_jwt_token:
    print("Generated IAP JWT Token:")
    print(iap_jwt_token)
else:
    print("Failed to generate IAP JWT Token.")
