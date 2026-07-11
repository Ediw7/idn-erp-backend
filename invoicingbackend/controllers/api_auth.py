import json
from odoo import http
from odoo.http import request, Response


class AuthController(http.Controller):

    @http.route(
        "/api/auth/login",
        type="http",
        auth="public",
        methods=["POST", "OPTIONS"],
        csrf=False,
        cors="*",
    )
    def login(self, **kwargs):
        # Handle CORS preflight OPTIONS request gracefully if needed
        if request.httprequest.method == "OPTIONS":
            return Response(status=200)

        try:
            # Parse request body from React/Axios
            data = json.loads(request.httprequest.data.decode("utf-8"))
            db = data.get("db")  # Odoo needs a database name to authenticate
            login = data.get("login")
            password = data.get("password")

            if not db or not login or not password:
                return Response(
                    json.dumps({"error": "Missing db, login, or password"}),
                    status=400,
                    content_type="application/json",
                )

            # Authenticate and set session cookie
            uid = request.session.authenticate(db, login, password)
            if not uid:
                return Response(
                    json.dumps({"error": "Invalid credentials"}),
                    status=401,
                    content_type="application/json",
                )

            # Retrieve user context to send back basic info
            user = request.env["res.users"].sudo().browse(uid)

            response = Response(
                json.dumps(
                    {
                        "message": "Login successful",
                        "uid": uid,
                        "session_id": request.session.sid,
                        "company_id": request.env.company.id,
                        "user": {
                            "name": user.name,
                            "email": user.login,
                            "is_admin": user.has_group("base.group_erp_manager"),
                            "company_name": (
                                user.company_id.name
                                if user.company_id
                                else "PT. EDI Accounting System"
                            ),
                        },
                    }
                ),
                status=200,
                content_type="application/json",
            )
            response.set_cookie(
                "session_id", request.session.sid, httponly=True, samesite="Lax"
            )
            return response
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )

    @http.route(
        "/api/auth/register",
        type="http",
        auth="public",
        methods=["POST", "OPTIONS"],
        csrf=False,
        cors="*",
    )
    def register(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return Response(status=200)

        try:
            data = json.loads(request.httprequest.data.decode("utf-8"))
            db = data.get("db", "ediaccounting")
            name = data.get("name")
            company_name = data.get("company_name")
            login = data.get("login")
            password = data.get("password")

            if not name or not company_name or not login or not password:
                return Response(
                    json.dumps(
                        {"error": "Missing name, company_name, login, or password"}
                    ),
                    status=400,
                    content_type="application/json",
                )

            import odoo

            registry = odoo.registry(db)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                existing_user = (
                    env["res.users"]
                    .with_context(active_test=False)
                    .search([("login", "=ilike", login)])
                )
                if existing_user:
                    return Response(
                        json.dumps(
                            {
                                "error": f"User dengan email {login} sudah terdaftar di sistem."
                            }
                        ),
                        status=400,
                        content_type="application/json",
                    )

                # --- TRANSAKSI ATOMIK MULTI-TENANT ---
                # 1. Bikin Ruang Perusahaan (Tenant)
                new_company = env["res.company"].create(
                    {
                        "name": company_name,
                    }
                )

                # 2. Bikin Akun User & Ikatkan ke Tenant
                group_user = env.ref("base.group_user")
                new_user = env["res.users"].create(
                    {
                        "name": name,
                        "login": login,
                        "password": password,
                        "company_id": new_company.id,
                        "company_ids": [(4, new_company.id)],
                        "groups_id": [(6, 0, [group_user.id])],
                    }
                )
                uid = new_user.id

            return Response(
                json.dumps({"message": "Registration successful", "uid": uid}),
                status=200,
                content_type="application/json",
            )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )

    @http.route(
        "/api/auth/users",
        type="http",
        auth="public",
        methods=["GET", "OPTIONS"],
        csrf=False,
        cors="*",
    )
    def get_users(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return Response(status=200)

        if not request.session.uid:
            return Response(
                json.dumps({"error": "Session expired or unauthorized"}),
                status=401,
                content_type="application/json",
            )

        try:
            if (
                not request.env["res.users"]
                .sudo()
                .browse(request.session.uid)
                .has_group("base.group_erp_manager")
            ):
                return Response(
                    json.dumps({"error": "Access Denied"}),
                    status=403,
                    content_type="application/json",
                )

            users = request.env["res.users"].sudo().search([])
            data = []
            for u in users:
                data.append(
                    {
                        "id": u.id,
                        "name": u.name,
                        "login": u.login,
                        "is_admin": u.has_group("base.group_erp_manager"),
                        "is_active": u.active,
                    }
                )
            return Response(
                json.dumps({"status": "success", "data": data}),
                status=200,
                content_type="application/json",
            )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )

    @http.route(
        "/api/auth/users/toggle",
        type="http",
        auth="user",
        methods=["POST", "OPTIONS"],
        csrf=False,
        cors="*",
    )
    def toggle_user(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return Response(status=200)

        try:
            if not request.env.user.has_group("base.group_erp_manager"):
                return Response(
                    json.dumps({"error": "Access Denied"}),
                    status=403,
                    content_type="application/json",
                )

            data = json.loads(request.httprequest.data.decode("utf-8"))
            user_id = data.get("id")
            if not user_id:
                return Response(
                    json.dumps({"error": "Missing user ID"}),
                    status=400,
                    content_type="application/json",
                )

            # Prevent admin from deactivating themselves
            if user_id == request.env.user.id:
                return Response(
                    json.dumps({"error": "Cannot deactivate your own account"}),
                    status=400,
                    content_type="application/json",
                )

            user_record = request.env["res.users"].sudo().browse(user_id)
            if user_record.exists():
                user_record.active = not user_record.active
                return Response(
                    json.dumps(
                        {"status": "success", "message": "Status user berhasil diubah"}
                    ),
                    status=200,
                    content_type="application/json",
                )
            else:
                return Response(
                    json.dumps({"error": "User tidak ditemukan"}),
                    status=404,
                    content_type="application/json",
                )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )

    @http.route(
        "/api/auth/users/create",
        type="http",
        auth="user",
        methods=["POST", "OPTIONS"],
        csrf=False,
        cors="*",
    )
    def create_user(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return Response(status=200)

        try:
            if not request.env.user.has_group("base.group_erp_manager"):
                return Response(
                    json.dumps({"error": "Access Denied"}),
                    status=403,
                    content_type="application/json",
                )

            data = json.loads(request.httprequest.data.decode("utf-8"))
            name = data.get("name")
            login = data.get("login")
            password = data.get("password")
            company_name = data.get("company_name")
            is_admin = data.get("is_admin", False)

            if not name or not login or not password:
                return Response(
                    json.dumps({"error": "Missing name, login, or password"}),
                    status=400,
                    content_type="application/json",
                )

            existing_user = (
                request.env["res.users"]
                .sudo()
                .with_context(active_test=False)
                .search([("login", "=ilike", login)], limit=1)
            )

            # Handle Company
            company_id = request.env.user.company_id.id
            if company_name:
                existing_company = (
                    request.env["res.company"]
                    .sudo()
                    .search([("name", "=ilike", company_name)], limit=1)
                )
                if existing_company:
                    company_id = existing_company.id
                else:
                    new_company = (
                        request.env["res.company"].sudo().create({"name": company_name})
                    )
                    company_id = new_company.id

            group_id = (
                request.env.ref("base.group_erp_manager").id
                if is_admin
                else request.env.ref("base.group_user").id
            )

            if existing_user:
                if existing_user.active:
                    return Response(
                        json.dumps(
                            {
                                "error": f"User dengan email {login} sudah aktif terdaftar di sistem."
                            }
                        ),
                        status=400,
                        content_type="application/json",
                    )
                else:
                    # Restore archived user
                    existing_user.write(
                        {
                            "active": True,
                            "name": name,
                            "password": password,
                            "company_id": company_id,
                            "company_ids": [(4, company_id)],
                            "groups_id": [(6, 0, [group_id])],
                        }
                    )
                    return Response(
                        json.dumps(
                            {
                                "status": "success",
                                "message": "User lama yang terhapus berhasil dipulihkan",
                                "id": existing_user.id,
                            }
                        ),
                        status=200,
                        content_type="application/json",
                    )

            new_user = (
                request.env["res.users"]
                .sudo()
                .create(
                    {
                        "name": name,
                        "login": login,
                        "password": password,
                        "company_id": company_id,
                        "company_ids": [(4, company_id)],
                        "groups_id": [(6, 0, [group_id])],
                    }
                )
            )

            return Response(
                json.dumps(
                    {
                        "status": "success",
                        "message": "User berhasil dibuat",
                        "id": new_user.id,
                    }
                ),
                status=200,
                content_type="application/json",
            )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )

    @http.route(
        "/api/auth/users/update",
        type="http",
        auth="user",
        methods=["POST", "OPTIONS"],
        csrf=False,
        cors="*",
    )
    def update_user(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return Response(status=200)

        try:
            if not request.env.user.has_group("base.group_erp_manager"):
                return Response(
                    json.dumps({"error": "Access Denied"}),
                    status=403,
                    content_type="application/json",
                )

            data = json.loads(request.httprequest.data.decode("utf-8"))
            user_id = data.get("id")
            if not user_id:
                return Response(
                    json.dumps({"error": "Missing user ID"}),
                    status=400,
                    content_type="application/json",
                )

            user_record = request.env["res.users"].sudo().browse(user_id)
            if not user_record.exists():
                return Response(
                    json.dumps({"error": "User tidak ditemukan"}),
                    status=404,
                    content_type="application/json",
                )

            update_vals = {}
            if data.get("name"):
                update_vals["name"] = data["name"]
            if data.get("login"):
                update_vals["login"] = data["login"]
            if data.get("password"):
                update_vals["password"] = data["password"]

            if update_vals:
                user_record.write(update_vals)

            return Response(
                json.dumps(
                    {"status": "success", "message": "User berhasil diperbarui"}
                ),
                status=200,
                content_type="application/json",
            )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )

    @http.route(
        "/api/auth/users/delete",
        type="http",
        auth="user",
        methods=["POST", "OPTIONS"],
        csrf=False,
        cors="*",
    )
    def delete_user(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return Response(status=200)

        try:
            if not request.env.user.has_group("base.group_erp_manager"):
                return Response(
                    json.dumps({"error": "Access Denied"}),
                    status=403,
                    content_type="application/json",
                )

            data = json.loads(request.httprequest.data.decode("utf-8"))
            user_id = data.get("id")
            if not user_id:
                return Response(
                    json.dumps({"error": "Missing user ID"}),
                    status=400,
                    content_type="application/json",
                )

            if user_id == request.env.user.id:
                return Response(
                    json.dumps({"error": "Tidak bisa menghapus akun sendiri"}),
                    status=400,
                    content_type="application/json",
                )

            user_record = request.env["res.users"].sudo().browse(user_id)
            if user_record.exists():
                user_record.active = False  # Soft delete (archive) for safety
                return Response(
                    json.dumps(
                        {"status": "success", "message": "User berhasil dihapus"}
                    ),
                    status=200,
                    content_type="application/json",
                )
            else:
                return Response(
                    json.dumps({"error": "User tidak ditemukan"}),
                    status=404,
                    content_type="application/json",
                )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json",
            )

    @http.route(
        "/api/auth/logout",
        type="http",
        auth="public",
        methods=["POST", "OPTIONS"],
        csrf=False,
        cors="*",
    )
    def logout(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return Response(status=200)

        request.session.logout(keep_db=True)
        return Response(
            json.dumps({"message": "Logged out successfully"}),
            status=200,
            content_type="application/json",
        )
