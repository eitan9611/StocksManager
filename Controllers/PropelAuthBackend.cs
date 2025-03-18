using Backend.Services;
using Backend.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace PropelAuthBackend.Controllers
{
    [Route("api/secure")]
    [ApiController]
    public class SecureController : ControllerBase
    {
        private readonly ISecureService _secureService;

        public SecureController(ISecureService secureService)
        {
            _secureService = secureService;
        }

        [HttpGet]
        [Authorize]
        public ActionResult<SecureData> GetSecureData()
        {
            var message = _secureService.GetSecureMessage();
            var data = new SecureData { Message = message };
            return Ok(data);
        }
    }


}
