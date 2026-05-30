import json
from odoo import http
from odoo.http import request, Response

class AuthController(http.Controller):

    @http.route('/api/auth/login', type='http', auth='public', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def login(self, **kwargs):
        # Handle CORS preflight OPTIONS request gracefully if needed
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200)

        try:
            # Parse request body from React/Axios
            data = json.loads(request.httprequest.data.decode('utf-8'))
            db = data.get('db') # Odoo needs a database name to authenticate
            login = data.get('login')
            password = data.get('password')

            if not db or not login or not password:
                return Response(
                    json.dumps({'error': 'Missing db, login, or password'}), 
                    status=400, 
                    content_type='application/json'
                )

            # Authenticate and set session cookie
            uid = request.session.authenticate(db, login, password)
            if not uid:
                return Response(
                    json.dumps({'error': 'Invalid credentials'}), 
                    status=401, 
                    content_type='application/json'
                )

            # Retrieve user context to send back basic info
            user = request.env['res.users'].sudo().browse(uid)
            
            return Response(
                json.dumps({
                    'message': 'Login successful',
                    'uid': uid,
                    'session_id': request.session.sid, # Also sent as a Set-Cookie header automatically
                    'company_id': request.env.company.id,
                    'user': {
                        'name': user.name,
                        'email': user.login
                    }
                }),
                status=200,
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'error': str(e)}), 
                status=500, 
                content_type='application/json'
            )

    @http.route('/api/auth/logout', type='http', auth='public', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def logout(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200)
            
        request.session.logout(keep_db=True)
        return Response(
            json.dumps({'message': 'Logged out successfully'}), 
            status=200, 
            content_type='application/json'
        )
