"""Minimal Home Assistant stubs to allow audi_connect_ha to import"""
import sys
from types import ModuleType
from enum import Enum
from datetime import datetime, timezone

# Create mock module hierarchy
homeassistant = ModuleType('homeassistant')

# Create helpers submodules
homeassistant.helpers = ModuleType('homeassistant.helpers')
# Create a custom module class that provides passthrough functions for missing attributes
class ConfigValidationModule(ModuleType):
    """Module that provides passthrough validators for any missing attributes"""
    def __getattr__(self, name):
        # Return a passthrough function for any missing validator
        def passthrough(*args, **kwargs):
            if args:
                return args[0]  # Return first argument if provided
            return lambda x: x  # Otherwise return identity function
        return passthrough

homeassistant.helpers.config_validation = ConfigValidationModule('homeassistant.helpers.config_validation')
homeassistant.helpers.event = ModuleType('homeassistant.helpers.event')
homeassistant.helpers.aiohttp_client = ModuleType('homeassistant.helpers.aiohttp_client')
homeassistant.helpers.dispatcher = ModuleType('homeassistant.helpers.dispatcher')
homeassistant.helpers.entity = ModuleType('homeassistant.helpers.entity')
homeassistant.helpers.entity_platform = ModuleType('homeassistant.helpers.entity_platform')
homeassistant.helpers.device_registry = ModuleType('homeassistant.helpers.device_registry')

# Create components submodules
homeassistant.components = ModuleType('homeassistant.components')
homeassistant.components.sensor = ModuleType('homeassistant.components.sensor')
homeassistant.components.binary_sensor = ModuleType('homeassistant.components.binary_sensor')
homeassistant.components.lock = ModuleType('homeassistant.components.lock')
homeassistant.components.device_tracker = ModuleType('homeassistant.components.device_tracker')
homeassistant.components.device_tracker.config_entry = ModuleType('homeassistant.components.device_tracker.config_entry')

# Create other core modules
homeassistant.core = ModuleType('homeassistant.core')
homeassistant.util = ModuleType('homeassistant.util')
homeassistant.util.dt = ModuleType('homeassistant.util.dt')
homeassistant.config_entries = ModuleType('homeassistant.config_entries')
homeassistant.const = ModuleType('homeassistant.const')

# Add Platform enum
class Platform(str, Enum):
    SENSOR = "sensor"
    BINARY_SENSOR = "binary_sensor"
    SWITCH = "switch"
    DEVICE_TRACKER = "device_tracker"
    LOCK = "lock"

# Add SourceType enum
class SourceType(str, Enum):
    GPS = "gps"

# Add BinarySensorDeviceClass enum
class BinarySensorDeviceClass(str, Enum):
    PROBLEM = "problem"
    PLUG = "plug"
    DOOR = "door"
    WINDOW = "window"
    LOCK = "lock"

# Add SensorDeviceClass enum
class SensorDeviceClass(str, Enum):
    BATTERY = "battery"
    TEMPERATURE = "temperature"
    DISTANCE = "distance"
    DURATION = "duration"
    ENERGY = "energy"

# Add SensorStateClass enum
class SensorStateClass(str, Enum):
    MEASUREMENT = "measurement"
    TOTAL = "total"
    TOTAL_INCREASING = "total_increasing"

# Add Unit classes
class UnitOfTime(str, Enum):
    MINUTES = "min"
    HOURS = "h"
    DAYS = "d"

class UnitOfLength(str, Enum):
    KILOMETERS = "km"
    METERS = "m"
    MILES = "mi"

class UnitOfTemperature(str, Enum):
    CELSIUS = "°C"
    FAHRENHEIT = "°F"

class UnitOfPower(str, Enum):
    WATT = "W"
    KILOWATT = "kW"

class UnitOfElectricCurrent(str, Enum):
    AMPERE = "A"

class EntityCategory(str, Enum):
    CONFIG = "config"
    DIAGNOSTIC = "diagnostic"

# String constants
PERCENTAGE = "%"

homeassistant.const.Platform = Platform
homeassistant.const.PERCENTAGE = PERCENTAGE
homeassistant.const.UnitOfTime = UnitOfTime
homeassistant.const.UnitOfLength = UnitOfLength
homeassistant.const.UnitOfTemperature = UnitOfTemperature
homeassistant.const.UnitOfPower = UnitOfPower
homeassistant.const.UnitOfElectricCurrent = UnitOfElectricCurrent
homeassistant.const.EntityCategory = EntityCategory
homeassistant.components.device_tracker.SourceType = SourceType
homeassistant.components.binary_sensor.BinarySensorDeviceClass = BinarySensorDeviceClass
homeassistant.components.sensor.SensorDeviceClass = SensorDeviceClass
homeassistant.components.sensor.SensorStateClass = SensorStateClass

# Add minimal required attributes to const
homeassistant.const.CONF_NAME = 'name'
homeassistant.const.CONF_PASSWORD = 'password'
homeassistant.const.CONF_RESOURCES = 'resources'
homeassistant.const.CONF_SCAN_INTERVAL = 'scan_interval'
homeassistant.const.CONF_USERNAME = 'username'

# Add stub classes
class HomeAssistant:
    pass

class ConfigEntry:
    pass

class DeviceEntry:
    pass

class Entity:
    """Base entity class stub"""
    pass

class ToggleEntity(Entity):
    pass

class SensorEntity(Entity):
    pass

class BinarySensorEntity(Entity):
    pass

class LockEntity(Entity):
    pass

class TrackerEntity(Entity):
    pass

class DeviceInfo(dict):
    pass

class AddEntitiesCallback:
    pass

# Add stub functions and validators
def string(value):
    """String validator stub - just returns the value"""
    return str(value)

def positive_int(value):
    """Positive integer validator stub"""
    return int(value)

def boolean(value):
    """Boolean validator stub"""
    return bool(value)

def time_period(value):
    """Time period validator stub"""
    from datetime import timedelta
    if isinstance(value, timedelta):
        return value
    return timedelta(seconds=int(value))

def schema_with_slug_keys(*args, **kwargs):
    """Schema validator stub - returns a passthrough function"""
    return lambda x: x

def async_track_time_interval(*args, **kwargs):
    pass

def async_get_clientsession(*args, **kwargs):
    """Return the session object - not used in our standalone implementation"""
    return None

def async_dispatcher_send(*args, **kwargs):
    pass

def async_dispatcher_connect(*args, **kwargs):
    pass

def utcnow():
    return datetime.now(timezone.utc)

def callback(func):
    """Callback decorator stub"""
    return func

# Assign functions and classes to modules
homeassistant.helpers.config_validation.string = string
homeassistant.helpers.config_validation.positive_int = positive_int
homeassistant.helpers.config_validation.boolean = boolean
homeassistant.helpers.config_validation.time_period = time_period
homeassistant.helpers.config_validation.schema_with_slug_keys = schema_with_slug_keys
homeassistant.helpers.event.async_track_time_interval = async_track_time_interval
homeassistant.helpers.aiohttp_client.async_get_clientsession = async_get_clientsession
homeassistant.helpers.dispatcher.async_dispatcher_send = async_dispatcher_send
homeassistant.helpers.dispatcher.async_dispatcher_connect = async_dispatcher_connect
homeassistant.helpers.entity.Entity = Entity
homeassistant.helpers.entity.ToggleEntity = ToggleEntity
homeassistant.helpers.entity.DeviceInfo = DeviceInfo
homeassistant.helpers.entity_platform.AddEntitiesCallback = AddEntitiesCallback
homeassistant.util.dt.utcnow = utcnow
homeassistant.core.HomeAssistant = HomeAssistant
homeassistant.core.callback = callback
homeassistant.config_entries.ConfigEntry = ConfigEntry
homeassistant.helpers.device_registry.DeviceEntry = DeviceEntry
homeassistant.components.sensor.SensorEntity = SensorEntity
homeassistant.components.binary_sensor.BinarySensorEntity = BinarySensorEntity
homeassistant.components.lock.LockEntity = LockEntity
homeassistant.components.device_tracker.config_entry.TrackerEntity = TrackerEntity

# Register all modules in sys.modules
sys.modules['homeassistant'] = homeassistant
sys.modules['homeassistant.helpers'] = homeassistant.helpers
sys.modules['homeassistant.helpers.config_validation'] = homeassistant.helpers.config_validation
sys.modules['homeassistant.helpers.event'] = homeassistant.helpers.event
sys.modules['homeassistant.helpers.aiohttp_client'] = homeassistant.helpers.aiohttp_client
sys.modules['homeassistant.helpers.dispatcher'] = homeassistant.helpers.dispatcher
sys.modules['homeassistant.helpers.entity'] = homeassistant.helpers.entity
sys.modules['homeassistant.helpers.entity_platform'] = homeassistant.helpers.entity_platform
sys.modules['homeassistant.helpers.device_registry'] = homeassistant.helpers.device_registry
sys.modules['homeassistant.components'] = homeassistant.components
sys.modules['homeassistant.components.sensor'] = homeassistant.components.sensor
sys.modules['homeassistant.components.binary_sensor'] = homeassistant.components.binary_sensor
sys.modules['homeassistant.components.lock'] = homeassistant.components.lock
sys.modules['homeassistant.components.device_tracker'] = homeassistant.components.device_tracker
sys.modules['homeassistant.components.device_tracker.config_entry'] = homeassistant.components.device_tracker.config_entry
sys.modules['homeassistant.core'] = homeassistant.core
sys.modules['homeassistant.util'] = homeassistant.util
sys.modules['homeassistant.util.dt'] = homeassistant.util.dt
sys.modules['homeassistant.config_entries'] = homeassistant.config_entries
sys.modules['homeassistant.const'] = homeassistant.const
