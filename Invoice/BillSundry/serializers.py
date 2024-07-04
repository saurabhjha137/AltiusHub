from rest_framework import serializers
from .models import InvoiceHeader, InvoiceItem, InvoiceBillSundry

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        data['amount'] = data['quantity'] * data['price']
        return data

class InvoiceBillSundrySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceBillSundry
        fields = '__all__'

class InvoiceHeaderSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    billsundrys = InvoiceBillSundrySerializer(many=True)

    class Meta:
        model = InvoiceHeader
        fields = '__all__'

    def validate(self, data):
        items = data.get('items', [])
        for item in items:
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than zero.")
            if item['price'] <= 0:
                raise serializers.ValidationError("Price must be greater than zero.")
            item['amount'] = item['quantity'] * item['price']
        
        data['total_amount'] = sum(item['amount'] for item in items) + sum(bill['amount'] for bill in data.get('billsundrys', []))
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        billsundrys_data = validated_data.pop('billsundrys')
        invoice = InvoiceHeader.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        for billsundry_data in billsundrys_data:
            InvoiceBillSundry.objects.create(invoice=invoice, **billsundry_data)
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        billsundrys_data = validated_data.pop('billsundrys')

        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.billing_address = validated_data.get('billing_address', instance.billing_address)
        instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
        instance.gstin = validated_data.get('gstin', instance.gstin)
        instance.save()

        instance.items.all().delete()
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=instance, **item_data)

        instance.billsundrys.all().delete()
        for billsundry_data in billsundrys_data:
            InvoiceBillSundry.objects.create(invoice=instance, **billsundry_data)

        instance.total_amount = sum(item['amount'] for item in items_data) + sum(bill['amount'] for bill in billsundrys_data)
        instance.save()
        return instance
