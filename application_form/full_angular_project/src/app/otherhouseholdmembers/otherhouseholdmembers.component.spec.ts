
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { OtherHouseholdMembersComponent } from './otherhouseholdmembers.component';
import { By } from '@angular/platform-browser';

describe('OtherHouseholdMembersComponent', () => {
  let component: OtherHouseholdMembersComponent;
  let fixture: ComponentFixture<OtherHouseholdMembersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [OtherHouseholdMembersComponent],
      imports: [ReactiveFormsModule],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OtherHouseholdMembersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize the form', () => {
    expect(component.form).toBeDefined();
    expect(component.form.controls['name']).toBeDefined();
    expect(component.form.controls['age']).toBeDefined();
    expect(component.form.controls['relationship']).toBeDefined();
  });

  it('should mark the form as invalid if required fields are empty', () => {
    component.form.controls['name'].setValue('');
    component.form.controls['age'].setValue('');
    component.form.controls['relationship'].setValue('');
    
    expect(component.form.valid).toBeFalsy();
  });

  it('should mark the form as valid when all fields are filled', () => {
    component.form.controls['name'].setValue('John Doe');
    component.form.controls['age'].setValue(30);
    component.form.controls['relationship'].setValue('Brother');
    
    expect(component.form.valid).toBeTruthy();
  });

  it('should submit the form', () => {
    spyOn(component, 'onSubmit');
    
    component.form.controls['name'].setValue('John Doe');
    component.form.controls['age'].setValue(30);
    component.form.controls['relationship'].setValue('Brother');
    
    fixture.debugElement.query(By.css('form')).triggerEventHandler('ngSubmit', null);
    
    expect(component.onSubmit).toHaveBeenCalled();
  });

  it('should reset the form on reset', () => {
    component.form.controls['name'].setValue('John Doe');
    component.form.controls['age'].setValue(30);
    component.form.controls['relationship'].setValue('Brother');

    component.onReset();
    
    expect(component.form.controls['name'].value).toBe('');
    expect(component.form.controls['age'].value).toBe('');
    expect(component.form.controls['relationship'].value).toBe('');
  });
});
