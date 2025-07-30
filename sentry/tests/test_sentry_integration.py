# Test Sentry Integration Script
# This script creates intentional errors to test the Sentry integration

import logging
import traceback

from odoo import api, models, _
from odoo.exceptions import UserError, ValidationError, AccessError

_logger = logging.getLogger(__name__)


class SentryTestWizard(models.TransientModel):
    _name = 'sentry.test.wizard'
    _description = 'Sentry Integration Test Wizard'

    @api.model
    def test_error_logging(self):
        """Test basic error logging to Sentry"""
        _logger.error("Test error message from Odoo to Sentry")
        return True

    @api.model
    def test_warning_logging(self):
        """Test warning logging to Sentry"""
        _logger.warning("Test warning message from Odoo to Sentry")
        return True

    @api.model
    def test_exception_capture(self):
        """Test exception capture in Sentry"""
        try:
            # Intentionally cause a division by zero
            result = 1 / 0
        except ZeroDivisionError as e:
            _logger.error("Division by zero error: %s", str(e), exc_info=True)
            raise UserError(_("This is a test exception for Sentry integration"))

    @api.model
    def test_validation_error(self):
        """Test ValidationError (should be ignored by default)"""
        raise ValidationError(_("This ValidationError should be ignored by Sentry"))

    @api.model
    def test_access_error(self):
        """Test AccessError (should be ignored by default)"""
        raise AccessError(_("This AccessError should be ignored by Sentry"))

    @api.model
    def test_custom_context(self):
        """Test custom context data in Sentry"""
        try:
            # Add custom context
            import sentry_sdk
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("test_type", "custom_context")
                scope.set_extra("custom_data", {
                    "user_id": self.env.user.id,
                    "company_id": self.env.company.id,
                    "test_timestamp": str(self.env.cr.now())
                })
                scope.set_user({
                    "id": self.env.user.id,
                    "username": self.env.user.login,
                    "email": self.env.user.email
                })
            
            # Trigger an error with custom context
            raise Exception("Test exception with custom context for Sentry")
            
        except Exception as e:
            _logger.error("Test exception with context: %s", str(e), exc_info=True)
            return True
