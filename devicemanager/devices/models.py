from django.core.validators import MinValueValidator
from django.db import models

class PowerSupply(models.Model):
    TYPES = [
        ('USB', 'USB'),
        ('EXTERNAL', 'EXTERNAL'),
    ]

    num = models.IntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(0)]
    )
    type_ps = models.CharField(
        max_length=8,
        blank=False,
        null=False,
        choices=TYPES,
        verbose_name="Type of Power Supply"
    )
    voltage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Value must be informed in Volts (V)"
    )
    max_current = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=True,
        null=True,
        help_text="Value must be informed in Ampere (A)"
    )
    available = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'power_supply'
        ordering = ['num']
        verbose_name = "Power supply"
        verbose_name_plural = "Power Suppliers" 

    def __str__(self):
        return 'Power Supply ' + str(self.num)

class SerialCollector(models.Model):
    TYPES = [
        ('INTEGRATED', 'INTEGRATED'),
        ('EXTERNAL', 'EXTERNAL'),
    ]

    name = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    serial_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    type_sc = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        choices=TYPES,
        verbose_name="Type of Serial Collector"
    )
    available = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )
    connected_power_supply = models.ForeignKey(
        PowerSupply,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        db_table = 'serial_collector'
        ordering = ['name']
        verbose_name = "Serial Collector"
        verbose_name_plural = "Serial Collectors" 

    def __str__(self):
        return self.name

class FPGA(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    manufacturer = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    serial_number = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    startup_time = models.IntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(0)],
        verbose_name="Startup time",
        help_text="Time required (in seconds) for the FPGA to initialize and be able to be programmed"
    ) 
    available = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )
    connected_power_supply = models.ForeignKey(
        PowerSupply,
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )
    connected_serial_collector = models.ForeignKey(
        SerialCollector,
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        db_table = 'fpga'
        ordering = ['name']
        verbose_name = "FPGA"
        verbose_name_plural = "FPGAs" 

    def __str__(self):
        return self.name
